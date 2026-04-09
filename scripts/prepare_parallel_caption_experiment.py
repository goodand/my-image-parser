#!/usr/bin/env python3
"""Materialize non-overlapping shard inputs for a parallel caption experiment."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class DatasetSpec:
    dataset_id: str
    dataset_jsonl: Path
    rows: list[dict[str, Any]]


@dataclass
class WorkerShard:
    worker_id: str
    dataset_id: str
    dataset_jsonl: str
    shard_jsonl: str
    output_ledger: str
    output_responses_dir: str
    row_count: int
    first_image_id: str | None
    last_image_id: str | None
    row_indexes: list[int]
    packet_path: str


class ShardPlanner:
    """Split datasets across workers while keeping each row in exactly one shard."""

    def __init__(self, workers: int) -> None:
        if workers < 1:
            raise ValueError("--workers must be at least 1.")
        self.workers = workers

    def allocate_workers(self, datasets: list[DatasetSpec]) -> dict[str, int]:
        if not datasets:
            raise ValueError("At least one dataset is required.")
        total_rows = sum(len(dataset.rows) for dataset in datasets)
        if total_rows == 0:
            raise ValueError("Datasets contain no rows.")
        if self.workers < len(datasets):
            raise ValueError("Worker count must be >= number of datasets.")

        exact_targets = {
            dataset.dataset_id: (len(dataset.rows) / total_rows) * self.workers
            for dataset in datasets
        }
        allocations: dict[str, int] = {
            dataset.dataset_id: max(1, int(exact_targets[dataset.dataset_id]))
            for dataset in datasets
        }
        current_total = sum(allocations.values())

        if current_total > self.workers:
            raise ValueError("Minimum-per-dataset allocation exceeds total workers.")

        remaining = self.workers - current_total
        if remaining == 0:
            return allocations

        ranked = sorted(
            datasets,
            key=lambda dataset: (
                exact_targets[dataset.dataset_id] - int(exact_targets[dataset.dataset_id]),
                len(dataset.rows),
            ),
            reverse=True,
        )
        for index in range(remaining):
            dataset = ranked[index % len(ranked)]
            allocations[dataset.dataset_id] += 1
        return allocations

    @staticmethod
    def split_rows(rows: list[dict[str, Any]], shard_count: int) -> list[list[tuple[int, dict[str, Any]]]]:
        base = len(rows) // shard_count
        remainder = len(rows) % shard_count
        chunks: list[list[tuple[int, dict[str, Any]]]] = []
        start = 0
        indexed_rows = list(enumerate(rows, start=1))
        for shard_index in range(shard_count):
            extra = 1 if shard_index < remainder else 0
            end = start + base + extra
            chunks.append(indexed_rows[start:end])
            start = end
        return chunks


class ExperimentMaterializer:
    """Write shard JSONL files, per-worker packets, and an aggregate manifest."""

    def __init__(
        self,
        *,
        root_dir: Path,
        shard_dir: Path,
        packet_dir: Path,
        output_ledger_dir: Path,
        phase_name: str,
        model: str,
    ) -> None:
        self.root_dir = root_dir
        self.shard_dir = shard_dir
        self.packet_dir = packet_dir
        self.output_ledger_dir = output_ledger_dir
        self.phase_name = phase_name
        self.model = model

    def make_worker_id(self, index: int) -> str:
        return f"w{index:02d}"

    def write_shard_jsonl(
        self,
        *,
        worker_id: str,
        dataset_id: str,
        indexed_rows: list[tuple[int, dict[str, Any]]],
    ) -> Path:
        path = self.shard_dir / f"{self.phase_name}_{dataset_id}_{worker_id}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [json.dumps(row, ensure_ascii=False) for _, row in indexed_rows]
        path.write_text(("\n".join(lines) + "\n") if lines else "", encoding="utf-8")
        return path

    def build_output_ledger(self, dataset_id: str, worker_id: str) -> Path:
        return self.output_ledger_dir / f"{self.phase_name}_{dataset_id}_{worker_id}.json"

    def write_packet(
        self,
        *,
        worker_id: str,
        dataset: DatasetSpec,
        shard_jsonl: Path,
        output_ledger: Path,
        indexed_rows: list[tuple[int, dict[str, Any]]],
    ) -> Path:
        packet_path = self.packet_dir / (
            f"TASK_PACKET_{self.phase_name}_{dataset.dataset_id}_{worker_id}.json"
        )
        packet_path.parent.mkdir(parents=True, exist_ok=True)
        packet = {
            "packet_profile": "issued",
            "task_family": "image_caption_experiment_parallel_worker",
            "task_id": f"TASK-{self.phase_name.upper()}-{dataset.dataset_id.upper()}-{worker_id.upper()}",
            "title": f"{self.phase_name} {dataset.dataset_id} {worker_id}",
            "goal": "Run one non-overlapping shard of the extracted-media OpenAI caption experiment.",
            "worker_id": worker_id,
            "dataset_id": dataset.dataset_id,
            "context_files": [
                "control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md",
                "control/project_domain/resources/master_plans/drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md",
                "control/project_domain/resources/experiment_plans/PLAN_phase1_caption_experiment_parallel_execution-at2026-03-27-18-31.md",
            ],
            "allowed_paths": [
                str(shard_jsonl.relative_to(self.root_dir)),
                str(output_ledger.relative_to(self.root_dir)),
                str(output_ledger.parent.relative_to(self.root_dir)),
            ],
            "locked_paths": [
                str(shard_jsonl.relative_to(self.root_dir)),
                str(output_ledger.relative_to(self.root_dir)),
                str((output_ledger.parent / f"{output_ledger.stem}_responses").relative_to(self.root_dir)),
            ],
            "constraints": {
                "do_not_touch_other_worker_ledgers": True,
                "do_not_edit_canonical_docs": True,
                "model": self.model,
            },
            "command": [
                "python3",
                "scripts/caption_images_openai.py",
                "--dataset-jsonl",
                str(shard_jsonl.relative_to(self.root_dir)),
                "--output",
                str(output_ledger.relative_to(self.root_dir)),
                "--model",
                self.model,
                "--detail",
                "high",
            ],
            "expected_rows": len(indexed_rows),
            "row_indexes": [index for index, _ in indexed_rows],
            "first_image_id": indexed_rows[0][1].get("image_id") if indexed_rows else None,
            "last_image_id": indexed_rows[-1][1].get("image_id") if indexed_rows else None,
            "done_definition": [
                "Only this worker ledger and sidecars are written.",
                "Status summary is readable from the worker ledger.",
                "No overlap exists with other worker shards or ledgers.",
            ],
            "created_at": utc_timestamp(),
        }
        packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return packet_path

    def materialize(self, datasets: list[DatasetSpec], allocations: dict[str, int]) -> dict[str, Any]:
        shards: list[WorkerShard] = []
        seen_image_ids: set[str] = set()
        seen_output_ledgers: set[str] = set()
        worker_index = 1

        for dataset in datasets:
            chunks = ShardPlanner.split_rows(dataset.rows, allocations[dataset.dataset_id])
            for indexed_rows in chunks:
                worker_id = self.make_worker_id(worker_index)
                worker_index += 1
                shard_jsonl = self.write_shard_jsonl(
                    worker_id=worker_id,
                    dataset_id=dataset.dataset_id,
                    indexed_rows=indexed_rows,
                )
                output_ledger = self.build_output_ledger(dataset.dataset_id, worker_id)
                packet_path = self.write_packet(
                    worker_id=worker_id,
                    dataset=dataset,
                    shard_jsonl=shard_jsonl,
                    output_ledger=output_ledger,
                    indexed_rows=indexed_rows,
                )
                row_indexes = [index for index, _ in indexed_rows]
                image_ids = [row.get("image_id") for _, row in indexed_rows if row.get("image_id")]
                overlap_ids = sorted(set(image_ids) & seen_image_ids)
                if overlap_ids:
                    raise RuntimeError(f"Image overlap detected for {worker_id}: {overlap_ids}")
                seen_image_ids.update(image_ids)
                output_key = str(output_ledger)
                if output_key in seen_output_ledgers:
                    raise RuntimeError(f"Ledger overlap detected: {output_key}")
                seen_output_ledgers.add(output_key)
                shards.append(
                    WorkerShard(
                        worker_id=worker_id,
                        dataset_id=dataset.dataset_id,
                        dataset_jsonl=str(dataset.dataset_jsonl),
                        shard_jsonl=str(shard_jsonl),
                        output_ledger=str(output_ledger),
                        output_responses_dir=str(output_ledger.parent / f"{output_ledger.stem}_responses"),
                        row_count=len(indexed_rows),
                        first_image_id=image_ids[0] if image_ids else None,
                        last_image_id=image_ids[-1] if image_ids else None,
                        row_indexes=row_indexes,
                        packet_path=str(packet_path),
                    )
                )

        manifest = {
            "phase_name": self.phase_name,
            "generated_at": utc_timestamp(),
            "worker_count": len(shards),
            "model": self.model,
            "datasets": [
                {
                    "dataset_id": dataset.dataset_id,
                    "dataset_jsonl": str(dataset.dataset_jsonl),
                    "row_count": len(dataset.rows),
                    "allocated_workers": allocations[dataset.dataset_id],
                }
                for dataset in datasets
            ],
            "overlap_checks": {
                "unique_image_ids": len(seen_image_ids),
                "unique_output_ledgers": len(seen_output_ledgers),
                "status": "ok",
            },
            "shards": [asdict(shard) for shard in shards],
        }
        manifest_path = self.shard_dir / f"{self.phase_name}_manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest["manifest_path"] = str(manifest_path)
        return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create non-overlapping shard inputs and worker packets for a parallel caption experiment."
    )
    parser.add_argument(
        "--dataset-jsonl",
        action="append",
        type=Path,
        required=True,
        help="One or more dataset JSONL inputs. Repeat the flag to add multiple datasets.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=10,
        help="Total worker count across all datasets.",
    )
    parser.add_argument(
        "--phase-name",
        default="phase1_caption_10w",
        help="Stable prefix for shard and packet outputs.",
    )
    parser.add_argument(
        "--model",
        default="gpt-4.1",
        help="Caption model recorded into worker packets.",
    )
    return parser.parse_args()


def load_dataset(dataset_jsonl: Path) -> DatasetSpec:
    resolved = dataset_jsonl.resolve()
    rows = [
        json.loads(line)
        for line in resolved.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    dataset_id = resolved.parent.parent.name
    return DatasetSpec(dataset_id=dataset_id, dataset_jsonl=resolved, rows=rows)


def main() -> int:
    args = parse_args()
    root_dir = Path(__file__).resolve().parents[1]
    datasets = [load_dataset(path) for path in args.dataset_jsonl]
    planner = ShardPlanner(args.workers)
    allocations = planner.allocate_workers(datasets)
    materializer = ExperimentMaterializer(
        root_dir=root_dir,
        shard_dir=root_dir / "control" / "project_domain" / "runs" / "manifests" / f"{args.phase_name}_shards",
        packet_dir=root_dir / "control" / "project_agent_ops" / "resources" / "task_packets" / "issued",
        output_ledger_dir=root_dir / "control" / "project_agent_ops" / "registry" / "runs" / "image_caption_jobs",
        phase_name=args.phase_name,
        model=args.model,
    )
    manifest = materializer.materialize(datasets, allocations)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
