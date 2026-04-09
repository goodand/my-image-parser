# Caption Comparison Review Sheet

## Purpose

이미지 캡션 후보를 evidence와 함께 나란히 검토하고 최종 선택을 기록하기 위한 Markdown 템플릿.

## Review Rules

- 원본 이미지와 evidence를 먼저 보고 캡션을 읽는다.
- 캡션 문장 자체보다 grounding 품질을 우선 본다.
- 선택 이유는 짧지만 재검토 가능하게 남긴다.

## Image Context

- Image ID:
- Source path:
- Related note:
- Review date:
- Reviewer:

## Image Preview

```md
![[relative/or/obsidian/image/path.png]]
```

## Evidence Summary

- Parser evidence:
- OCR evidence:
- Structural hints:
- Known uncertainty:

## Candidate Comparison

| Candidate | Caption | Strengths | Weaknesses | Grounding confidence |
| --- | --- | --- | --- | --- |
| A | [caption] | [strength] | [weakness] | [high/med/low] |
| B | [caption] | [strength] | [weakness] | [high/med/low] |
| C | [caption] | [strength] | [weakness] | [high/med/low] |
| D | [caption] | [strength] | [weakness] | [high/med/low] |

## Side-By-Side Review Notes

### Candidate A

- Good:
- Bad:
- Missing:

### Candidate B

- Good:
- Bad:
- Missing:

### Candidate C

- Good:
- Bad:
- Missing:

### Candidate D

- Good:
- Bad:
- Missing:

## Decision

- Selected candidate:
- Final caption:
- Why selected:
- Why others were rejected:

## Follow-Up

- Needs rewrite:
- Needs re-caption:
- Needs more OCR/parser evidence:
- Ready for commit:
