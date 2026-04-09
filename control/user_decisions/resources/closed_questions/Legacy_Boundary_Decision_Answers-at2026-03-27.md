# Legacy 경계 설계 — 의사결정 기록

> 작성 목적: LLM 기반 코드 생성 환경에서 legacy 경계를 강제하기 위한 구조 설계 결정 사항 기록

---

## 상위 철학 (모든 하위 결정의 기준)

| 축 | 결정 | 의미 |
|---|---|---|
| 신뢰 기반 vs 구조 기반 | **구조 기반** | 읽게 하는 것이 아니라 잘못 만들 수 없게 한다 |
| 지금 막기 vs 나중 제거 가능 | **나중에 제거 가능하게** | 즉각 차단보다 장기적으로 legacy를 제거할 수 있는 구조 우선 |

> 이 두 가지 철학이 아래 Q3, Q4, Q7, Q10을 자동으로 결정한다.

---

## 결정 상세 — 10개 질문

### 레이어 1 — 구조 강제 (즉각 효과)

#### Q3. shim re-export-only 강제
- **결정: 예**
- shim 파일 내부에 새 로직 추가 금지
- `old path`는 오직 `export * from '...'` 만 허용
- 근거: shim은 브리지일 뿐이며, 브리지에 로직이 쌓이면 브리지가 목적지가 된다

#### Q4. generator 강제
- **결정: 예 — CLI 스크립트 방식 (`npm run new:module`)**
- 빈 파일 직접 생성 금지, generator를 통해서만 파일 생성 허용
- generator가 실행 시점에 유사 파일 검색 및 중복 감지 수행
- 근거: LLM이 `touch` 또는 `fs.writeFile`로 직접 생성 시 CI에서 차단

```bash
npm run new:module -- --name PhotoRuntime
# → 유사 파일 검색
# → legacy shim 존재 확인
# → 같은 책임 디렉터리 확인
# → 통과 시에만 파일 생성
```

#### Q7. directory 경계 hard rule
- **결정: 예 — warning이 아닌 hard rule**
- 근거: 구조 기반 철학에서 자동 결정. warning은 LLM이 무시할 수 있다

---

### 레이어 2 — 감지 & 승인

#### Q1. shim에 새 import 예외 허용 시 승인 방식
- **결정: 코드 주석으로 이유 기록 + lint가 주석 존재 여부 확인**
- 예외는 허용하되, 이유가 코드에 반드시 남아야 통과

```js
// LEGACY-IMPORT: PhotoUtils 신규 대체 완료 전, 2024-Q2 제거 예정
import { oldPhotoHelper } from '../legacy/photoUtils'
```

- 주석 없이 import 시 lint 실패
- 구현: `eslint-rules/require-legacy-import-comment.js` 커스텀 룰

#### Q5. 유사 이름 중복 감지 차단 시점
- **결정: generator 실행 시점 (파일 만들기 전)**
- 함수명, 클래스명, 파일명, export 이름이 기존과 유사하면 생성 전 차단
- pre-commit이나 CI 단계가 아닌 가장 이른 시점에 막는다

#### Q8. directory contract 기계 판독 파일 도입 시점
- **결정: 지금 바로 도입**
- README.md만이 아닌 `CONTRACT.json` 또는 `ALLOWED.md` 형태의 기계 판독 규칙 파일 추가
- 근거: 구조 기반이니 먼저 깔아야 한다

```json
// src/services/photo/CONTRACT.json 예시
{
  "allowedFilePatterns": ["*.service.ts", "*.runtime.ts"],
  "forbiddenDependencies": ["../components", "../legacy"],
  "owner": "photo-runtime",
  "description": "photo runtime logic only"
}
```

---

### 레이어 3 — 장기 제거 가능성

#### Q9. allowlist + LLM 정기 갱신
- **결정: 예 — LLM이 정기적으로 갱신하게 설계**
- allowlist rot 방지: allowlist 자체가 legacy가 되지 않도록 LLM이 주기적으로 갱신
- 특정 디렉터리는 허용된 이름 패턴의 파일만 추가 가능

#### Q10. legacy 제거 기준 명문화
- **결정: 예**
- 제거 기준: `참조 0회 + 대체 경로 안정화 + 일정 기간 경고 없음`
- 근거: 나중에 제거 가능하게 하려면 제거 조건이 명문화되어야 한다

---

### 미결 — context 의존

아래 3개는 팀 상황 및 마이그레이션 진행 단계에 따라 조건부로 적용한다.

| Q | 내용 | 상태 |
|---|---|---|
| Q2 | LLM 의도 선언 강제 (재사용/확장/신규 중 선택) | context에 따라 다름 |
| Q6 | facade 파일 헤더 계약 (`Facade only` 주석) | context에 따라 다름 |
| Q7 세부 | no-restricted-imports 레이어별 적용 | 아래 별도 기술 |

---

## Q7 세부 — no-restricted-imports 레이어별 규칙

### 확정된 세 줄

| Rule | 방향 | 결정 | 근거 |
|---|---|---|---|
| Rule 1 | `services → components` | **hard block** | 서비스는 UI를 몰라야 함. 위반 시 단방향 의존 구조가 깨짐 |
| Rule 2 | `legacy → services` | **warn + 주석 강제** | 마이그레이션 중이라 허용 필요. 단, 이유가 기록되어야 통과 |
| Rule 3 | `components → legacy` | **warn + 주석 강제** | 일부 컴포넌트가 아직 이전 중. 새 코드가 legacy에 묶이면 제거 경로가 막힘 |

### eslint config 구현

```js
// .eslintrc.js
module.exports = {
  rules: {
    'no-restricted-imports': ['error', {
      patterns: [
        {
          // Rule 1: hard block
          group: ['*/components/*', '../components/*'],
          message:
            '[hard block] services → components import 금지. ' +
            '서비스는 UI에 의존할 수 없습니다.',
        },
      ],
    }],
  },

  overrides: [
    {
      // Rule 2: legacy → services, warn + 주석 강제
      files: ['src/legacy/**/*.{js,ts,tsx}'],
      rules: {
        'no-restricted-imports': ['warn', {
          patterns: [
            {
              group: ['*/services/*', '../services/*'],
              message:
                '[migration] legacy → services import 감지. ' +
                '이 줄 바로 위에 // LEGACY-IMPORT: <이유> 주석을 추가하세요.',
            },
          ],
        }],
      },
    },
    {
      // Rule 3: components → legacy, warn + 주석 강제
      files: ['src/components/**/*.{js,ts,tsx}'],
      rules: {
        'no-restricted-imports': ['warn', {
          patterns: [
            {
              group: ['*/legacy/*', '../legacy/*'],
              message:
                '[migration] components → legacy import 감지. ' +
                '이 줄 바로 위에 // LEGACY-IMPORT: <이유> 주석을 추가하세요.',
            },
          ],
        }],
      },
    },
  ],
}
```

### 주석 존재 여부 확인 커스텀 룰 (Q1 연동)

```js
// eslint-rules/require-legacy-import-comment.js
module.exports = {
  create(context) {
    return {
      ImportDeclaration(node) {
        const src = node.source.value
        const isLegacyImport =
          src.includes('/legacy/') || src.includes('../legacy/')
        if (!isLegacyImport) return

        const sourceCode = context.getSourceCode()
        const comments = sourceCode.getCommentsBefore(node)
        const hasMarker = comments.some(c =>
          c.value.trim().startsWith('LEGACY-IMPORT:')
        )

        if (!hasMarker) {
          context.report({
            node,
            message:
              'legacy import 바로 위에 // LEGACY-IMPORT: <이유> 주석이 없습니다.',
          })
        }
      },
    }
  },
}
```

---

## 결정 전체 요약

```
구조 기반 + 나중에 제거 가능하게
│
├── 레이어 1: 구조 강제
│   ├── Q3: shim re-export-only
│   ├── Q4: CLI generator 강제
│   └── Q7: directory 경계 hard rule
│
├── 레이어 2: 감지 & 승인
│   ├── Q1: 예외 시 주석 강제 + lint 확인
│   ├── Q5: generator 실행 시점 중복 차단
│   └── Q8: directory CONTRACT.json 즉시 도입
│
├── 레이어 3: 장기 제거
│   ├── Q9: allowlist + LLM 정기 갱신
│   └── Q10: 제거 기준 명문화
│
└── Q7 세부: no-restricted-imports
    ├── Rule 1 services → components: hard block
    ├── Rule 2 legacy → services:    warn + 주석
    └── Rule 3 components → legacy:  warn + 주석
```

> 핵심 원칙: warning보다 강한 해법은 "읽게 하는 것"이 아니라 "잘못 만들 수 없게 하는 것"이다.