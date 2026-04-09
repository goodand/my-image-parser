
# Data Flow 실행순서 계획서 초안

## 주제: PPT/PPTX 중심 멀티 변환 파이프라인

## 1. 목적

본 파이프라인의 목적은 `PPT/PPTX`를 입력으로 받아, 이를 **구조화된 중간표현(IR)** 으로 정규화한 뒤 아래 산출물 중 하나 이상으로 안정적으로 변환하는 것이다.

- Obsidian note set
    
- JS object / JSON AST
    
- Python object / dataclass
    
- Table
    
- worksheet(xlsx/csv)
    
- 이미지 기반 worksheet
    

또한 역방향 또는 후속 변환도 동일한 실행 프레임 안에서 다룬다.

- PPTX → Obsidian
    
- PPTX → JS
    
- JS → Obsidian
    
- PPTX → Python
    
- Python → Obsidian
    
- PPTX → Table
    
- PPTX → worksheet
    
- Image → worksheet
    

본 계획서는 특히 다음을 명확히 한다.

1. 실행 순서
    
2. 단계별 입력 / 처리 / 출력
    
3. 상태 저장 위치
    
4. 재실행 기준
    
5. 사람 검토 개입 지점
    

---

## 2. 설계 원칙

### 2.1 Source of Truth는 변환 결과 파일이 아니라 Canonical IR이다

Mermaid, Markdown, JS, Python, Obsidian note, worksheet는 모두 최종 산출물일 뿐이며, 운영 기준값은 **Canonical IR** 이다.

권장 IR 예시:

```json
{
  "job_id": "job_20260327_001",
  "source_type": "pptx",
  "document_id": "deck_001",
  "slides": [
    {
      "slide_id": "slide_001",
      "index": 1,
      "title": "Intro",
      "blocks": [
        {
          "block_id": "blk_001",
          "type": "text",
          "text": "Hello world"
        },
        {
          "block_id": "blk_002",
          "type": "image",
          "asset_id": "asset_001",
          "caption": null
        },
        {
          "block_id": "blk_003",
          "type": "table",
          "rows": [
            ["A", "B"],
            ["1", "2"]
          ]
        }
      ]
    }
  ],
  "assets": [
    {
      "asset_id": "asset_001",
      "kind": "image",
      "source_path": "slides/slide1/image1.png",
      "hash": "sha256:..."
    }
  ]
}
```

### 2.2 Skill / MCP / Worker 역할 분리

업로드된 기존 계획서 초안에서처럼, **orchestrator가 전체 실행을 잡고**, 상태와 진행률은 별도 레지스트리에서 관리하며, 실제 처리기는 하위 worker로 분리하는 구조를 유지한다. 또한 완료 판정은 worker의 자유형 응답이 아니라 **MCP에 저장된 상태값**으로 판단하는 방식이 안정적이다.

- **Skill**
    
    - 전체 오케스트레이션
        
    - 단계 순서 관리
        
    - 재시도 정책 적용
        
- **Registry / Execution MCP**
    
    - Job 상태
        
    - step 상태
        
    - artifact 위치
        
    - 오류 이력
        
- **Worker / Parser / Exporter**
    
    - 실제 parse / transform / export 수행
        

### 2.3 입력 본문은 최소화하고, 상태 조회는 Registry 기준으로 한다

기존 초안에서도 subagent 입력을 최소화하고 필요한 데이터는 Registry에서 조회하도록 설계했다. 이 원칙을 그대로 적용한다.

---

## 3. 범위

본 계획서는 아래 흐름을 포함한다.

### 3.1 Ingest 계열

- PPT/PPTX → Canonical IR
    
- Image → OCR/Table IR
    
- JS/Python object → Canonical IR
    

### 3.2 Export 계열

- Canonical IR → Obsidian
    
- Canonical IR → JS
    
- Canonical IR → Python
    
- Canonical IR → Table
    
- Canonical IR → worksheet
    

### 3.3 관리 계열

- Job 생성
    
- 상태 추적
    
- 검수
    
- 재실행
    
- 결과 패키징
    

---

## 4. 핵심 데이터 객체

기존 문서들이 `Job`, `Image Item`, `Execution Record`처럼 실행 단위와 상태 단위를 분리한 방식이 유용하므로, 여기서도 같은 패턴을 따른다.

### 4.1 Job

한 번의 변환 실행 단위

예시 필드:

- `job_id`
    
- `source_type`
    
- `source_uri`
    
- `requested_outputs`
    
- `status`
    
- `created_at`
    
- `pipeline_version`
    

예:

```json
{
  "job_id": "job_20260327_001",
  "source_type": "pptx",
  "source_uri": "/input/sample.pptx",
  "requested_outputs": ["obsidian", "js", "worksheet"],
  "status": "created",
  "pipeline_version": "v0.1"
}
```

### 4.2 Artifact Record

입력/중간/출력 산출물 관리용

- `artifact_id`
    
- `job_id`
    
- `artifact_type`
    
- `path`
    
- `format`
    
- `producer_step`
    
- `hash`
    

### 4.3 Execution Record

단계별 실행 상태

- `job_id`
    
- `step_name`
    
- `state`
    
- `attempt`
    
- `started_at`
    
- `finished_at`
    
- `last_error`
    
- `evidence`
    

예:

```json
{
  "job_id": "job_20260327_001",
  "step_name": "parse_pptx",
  "state": "queued",
  "attempt": 0,
  "started_at": null,
  "finished_at": null,
  "last_error": null,
  "evidence": []
}
```

### 4.4 IR Record

정규화된 문서 구조

- `document_id`
    
- `slides`
    
- `blocks`
    
- `assets`
    
- `relations`
    
- `validation_status`
    

---

## 5. 실행순서 기준 Data Flow

## Step 0. Job 생성 및 실행 준비

### 입력

- 사용자 요청
    
- 원본 파일 경로 또는 업로드 파일
    
- 원하는 출력 포맷 목록
    

### 처리

- `job_id` 발급
    
- requested outputs 기록
    
- 기본 step set 생성
    
- Registry에 Job 등록
    

### 출력

- `job_record.json`
    
- 초기 상태: `created`
    

### 비고

이 단계 이후부터 orchestrator는 로컬 변수보다 Registry를 기준으로 실행 상태를 조회한다는 점이 기존 계획서와 동일하다.

---

## Step 1. 입력 소스 수집 및 유형 판정

### 입력

- 원본 파일
    
- 확장자 / MIME / 메타데이터
    

### 처리

- 입력 타입 판정
    
    - `ppt`
        
    - `pptx`
        
    - `image`
        
    - `json/js`
        
    - `python`
        
- 구형 `.ppt`이면 사전 변환 필요 여부 기록
    
- 파일 해시 계산
    
- 소스 artifact 등록
    

### 출력

- `source_manifest.json`
    
- 상태: `source_registered`
    

### 분기

- `ppt/pptx`면 `Step 2A`로
    
- `image`면 `Step 2B`로
    
- `js/python`이면 `Step 2C`로
    

---

## Step 2A. PPT/PPTX Parsing

### 입력

- 원본 PPT/PPTX 파일
    

### 처리

- 슬라이드 단위 파싱
    
- text / image / table / shape 추출
    
- slide order 유지
    
- asset 분리 저장
    
- 파서별 raw output 보존
    

### 출력

- `parsed_pptx_raw.json`
    
- `extracted_assets/`
    
- 상태: `parsed_raw`
    

### 비고

이 단계는 “원본 문서 해석” 단계이며, 아직 Obsidian/JS/Python으로 직접 내보내지 않는다.

---

## Step 2B. Image Parsing / OCR / Table Detection

### 입력

- 이미지 파일
    

### 처리

- 이미지 메타데이터 추출
    
- OCR 실행
    
- 표 후보 탐지
    
- 셀 구조 복원 시도
    
- 실패 시 자유 텍스트 block로 fallback
    

### 출력

- `parsed_image_raw.json`
    
- `ocr_text.json`
    
- `detected_tables.json`
    
- 상태: `image_parsed`
    

---

## Step 2C. JS / Python 객체 로딩

### 입력

- JS object 또는 JSON
    
- Python dataclass / dict / serialized object
    

### 처리

- 로더 실행
    
- 필드 정합성 확인
    
- slide/block/asset 구조로 매핑
    

### 출력

- `loaded_structured_input.json`
    
- 상태: `structured_input_loaded`
    

---

## Step 3. Canonical IR 정규화

### 입력

- raw parse 결과
    
- asset 목록
    
- OCR/table 결과
    
- JS/Python 구조화 입력
    

### 처리

- 공통 slide/block schema로 정규화
    
- 텍스트 블록 정리
    
- 테이블 행/열 정규화
    
- 이미지 asset 연결
    
- heading/title 추론
    
- 원본 순서 보존
    
- provenance 필드 기록
    

### 출력

- `canonical_ir.json`
    
- 상태: `ir_normalized`
    

### 중요 규칙

이 단계의 `canonical_ir.json`이 이후 모든 exporter의 기준이 된다.

---

## Step 4. IR 검증 및 보정

### 입력

- `canonical_ir.json`
    

### 처리

- slide index 누락 검사
    
- block type 유효성 검사
    
- asset 참조 무결성 검사
    
- table 구조 검사
    
- 텍스트 인코딩 정리
    
- 중복 asset 병합 가능성 검사
    

### 출력

- `ir_validation_report.json`
    
- 상태:
    
    - `ir_validated`
        
    - 또는 `ir_needs_review`
        

### 사람 검토 가능 지점

- 제목 추론 오류
    
- 이미지-캡션 연결 오류
    
- 표 복원 실패
    
- decorative element 제거 여부
    

---

## Step 5. Export Plan 생성

### 입력

- `canonical_ir.json`
    
- requested outputs
    

### 처리

- 출력별 exporter 실행 계획 생성
    
- 예:
    
    - Obsidian exporter
        
    - JS exporter
        
    - Python exporter
        
    - table exporter
        
    - worksheet exporter
        
- 출력 간 의존성 계산
    

### 출력

- `export_plan.json`
    
- 상태: `export_planned`
    

### 예시

```json
{
  "job_id": "job_20260327_001",
  "exports": [
    {"target": "obsidian", "depends_on": ["ir_normalized"]},
    {"target": "js", "depends_on": ["ir_normalized"]},
    {"target": "worksheet", "depends_on": ["ir_normalized", "table_projection"]}
  ]
}
```

---

## Step 6. Obsidian Export

### 입력

- `canonical_ir.json`
    

### 처리

- slide 또는 section 기준 note split
    
- frontmatter 생성
    
- asset 경로 rewrite
    
- wiki-link 생성
    
- 필요 시 `.canvas` 생성
    
- note title slug 생성
    

### 출력

- `/obsidian_vault/*.md`
    
- `/obsidian_vault/assets/*`
    
- 필요 시 `/obsidian_vault/*.canvas`
    
- 상태: `obsidian_exported`
    

### 비고

이 단계에서 note granularity 정책을 고정해야 한다.

선택지:

- 1 deck = 1 note
    
- 1 slide = 1 note
    
- 1 section = 1 note
    

실무적으로는 `1 slide = 1 note`가 가장 추적하기 쉽다.

---

## Step 7. JS Export

### 입력

- `canonical_ir.json`
    

### 처리

- JS object literal 또는 JSON AST 생성
    
- block 타입별 serializer 적용
    
- asset reference를 상대경로 또는 URI로 변환
    

### 출력

- `deck.js`
    
- 또는 `deck.json`
    
- 상태: `js_exported`
    

---

## Step 8. Python Export

### 입력

- `canonical_ir.json`
    

### 처리

- dataclass / pydantic model / plain dict 중 선택
    
- slide/block/asset 객체 생성 코드 출력
    
- optional: 재생성용 builder 함수 포함
    

### 출력

- `deck.py`
    
- 상태: `python_exported`
    

---

## Step 9. Table Projection

### 입력

- `canonical_ir.json`
    

### 처리

- table block만 추출
    
- 텍스트 block을 행 기반 레코드로 평탄화
    
- slide/block provenance 유지
    
- 표가 없는 슬라이드는 summary row로 표현 가능
    

### 출력

- `tables.jsonl`
    
- `tables.csv`
    
- 상태: `table_projected`
    

### 비고

이 단계는 worksheet export의 전단계로 재사용 가능하다.

---

## Step 10. worksheet Export

### 입력

- `tables.jsonl`
    
- `canonical_ir.json`
    
- 필요 시 asset 경로
    

### 처리

- sheet 생성
    
- slide별 sheet 또는 테이블별 sheet 생성
    
- 셀 값 기록
    
- 이미지 첨부 여부 결정
    
- provenance column 추가
    
    - `slide_id`
        
    - `block_id`
        
    - `source_page`
        
    - `asset_id`
        

### 출력

- `output.xlsx`
    
- 또는 `output.csv`
    
- 상태: `worksheet_exported`
    

### 권장 규칙

- 분석용 sheet와 원본 보존용 sheet를 분리
    
- 첫 sheet는 summary
    
- 후속 sheet는 slide/table 단위
    

---

## Step 11. 최종 검증

### 입력

- 모든 exporter 결과
    
- `canonical_ir.json`
    

### 처리

- requested output 누락 여부 검사
    
- note 수와 slide 수 대응 검사
    
- JS/Python schema 일치 검사
    
- worksheet sheet 수 / table 수 검사
    
- asset broken link 검사
    

### 출력

- `final_validation_report.json`
    
- 상태:
    
    - `validated`
        
    - 또는 `validation_failed`
        

---

## Step 12. 산출물 패키징 및 완료 처리

### 입력

- 최종 산출물
    
- validation report
    

### 처리

- 결과 폴더 정리
    
- manifest 생성
    
- Registry 상태 갱신
    
- 재실행 필요 step 표시
    

### 출력

- `deliverables_manifest.json`
    
- 최종 상태: `completed`
    

---

## 6. 상태 흐름 초안

Job 상태는 아래 순서로 이동한다.

`created`  
→ `source_registered`  
→ `parsed_raw` 또는 `image_parsed` 또는 `structured_input_loaded`  
→ `ir_normalized`  
→ `ir_validated`  
→ `export_planned`  
→ `obsidian_exported` / `js_exported` / `python_exported` / `table_projected` / `worksheet_exported`  
→ `validated`  
→ `completed`

실패 시:

`running_step`  
→ `failed`  
→ `retry_queued`  
→ 재실행

---

## 7. 사람 개입 지점

기존 문서가 캡션 검토, 문서 매핑 검토, 이상치 설명 작성처럼 **사람 개입 구간을 별도 단계로 분리**한 점은 그대로 가져갈 가치가 있다. 여기서는 다음 구간을 사람 검토 지점으로 둔다.

### 검토 구간 A. IR 검토

- 제목 추론 확인
    
- 장식용 이미지 제거 여부
    
- table 복원 오류 수정
    

### 검토 구간 B. Obsidian 구조 검토

- note 분할 단위 확인
    
- frontmatter 적절성 확인
    
- link 구조 확인
    

### 검토 구간 C. worksheet 검토

- 셀 매핑 누락 확인
    
- 열 이름 정제
    
- 병합 셀 처리 검토
    

---

## 8. 재실행 정책

### 원칙

출력 전체를 다시 돌리지 않고 **step 단위 재실행** 가능해야 한다.

### 예시

- `parse_pptx` 실패
    
    - 최대 2회 재시도
        
- `ir_normalize` 실패
    
    - schema mismatch 해결 후 재실행
        
- `obsidian_export` 실패
    
    - exporter만 단독 재실행
        
- `worksheet_export` 실패
    
    - table projection 결과 유지 후 export만 재실행
        

### 중요 규칙

- 원본 artifact는 immutable
    
- `canonical_ir.json`은 버전 증가 방식으로 관리
    
- export 결과는 덮어쓰기보다 버전 디렉토리 권장
    

---

## 9. 권장 운영 규칙

1. **SubAgent/Worker 입력은 최소화한다**  
    `job_id`, `artifact_id`, `step_name` 정도만 전달한다. 이 원칙은 기존 실행 계획 문서와 동일하다.
    
2. **완료 여부는 Registry/MCP 조회로 판정한다**  
    worker 응답 텍스트는 참고용이다. 기존 문서도 이 원칙을 핵심으로 둔다.
    
3. **Parser와 Exporter를 분리한다**  
    `PPTX → IR` 과 `IR → Obsidian/JS/Python/worksheet`는 별개 단계다.
    
4. **모든 출력은 IR에서 파생한다**  
    `PPTX → Obsidian`과 `PPTX → JS`를 각각 직접 구현하지 말고, 둘 다 `IR`에서 내보낸다.
    
5. **Table과 worksheet는 별도 projection 단계를 둔다**  
    슬라이드 구조와 행/열 구조는 다르므로 한 번 평탄화가 필요하다.
    

---

## 10. 추천 모듈 구조

### Skill

- `ppt-ingest-orchestrator`
    
- `ir-normalizer`
    
- `obsidian-exporter`
    
- `js-exporter`
    
- `python-exporter`
    
- `worksheet-exporter`
    

### MCP / Registry

- execution status registry
    
- artifact registry
    
- optional: provenance registry
    

### Worker

- ppt parser worker
    
- image OCR worker
    
- table extractor worker
    
- markdown/obsidian renderer
    
- xlsx renderer
    

---

## 11. 한 줄 요약

이 파이프라인의 핵심은 다음이다.

**원본 PPT/PPTX나 이미지에서 직접 여러 포맷으로 흩어져 변환하지 말고, 먼저 Canonical IR로 정규화한 뒤, 모든 Obsidian/JS/Python/worksheet 산출물을 그 IR에서 파생시키며, 실행 상태와 완료 판정은 별도 Registry/MCP에서 관리한다.**

---

