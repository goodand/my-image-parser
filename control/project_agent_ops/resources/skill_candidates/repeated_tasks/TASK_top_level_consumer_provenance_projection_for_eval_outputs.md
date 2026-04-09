# TASK: Top-Level Consumer Provenance Projection For Eval Outputs

## Why this repeats

Consumer artifacts often already carry the right provenance, but only inside nested helper fields such as `input_resolution` or `batch_summary`. Downstream consumers then have to re-open nested structures just to learn the actual input mode, resolved bundle paths, or winner summary.

## Observed pattern

The stable output shape is easier to consume when the evaluation artifact projects a few key fields to the top level:
- `actual_input_mode`
- `requested_aggregate_bundle_paths`
- `resolved_per_image_bundle_paths`
- `winner_frequency`
- `baseline_retained`

## Current proven handling

Keep the richer nested structure, but also duplicate the most important consumer-facing provenance and batch summary fields at the top level of the canonical eval manifest.

## Promotion target

Reusable top-level provenance projection rule for consumer-facing eval outputs.

## Promotion trigger

Trigger promotion when another downstream manifest is structurally correct but still awkward to consume because its input truth and summary only live in nested helper sections.
