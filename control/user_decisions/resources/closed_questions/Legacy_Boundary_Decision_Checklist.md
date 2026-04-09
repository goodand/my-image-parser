
  1. 생성 전 게이트

  - 새 파일 만들기 전에 스크립트를 거치게 함
  - 예:
      - npm run new:module -- --name PhotoRuntime
  - 이 스크립트가
      - 유사 파일 검색
      - legacy shim 존재 확인
      - 같은 책임 디렉터리 확인
        를 먼저 하고, 통과할 때만 파일 생성

  2. restricted import

  - warning이 아니라 아예 import를 막음
  - 예:
      - no-restricted-imports
      - 특정 old path import 시 실패
  - handoff를 안 읽어도 강제로 멈춤

  3. directory contract

  - 각 디렉터리에 README.md만 두는 게 아니라
  - ALLOWED.md 또는 CONTRACT.json 같은 기계 판독 규칙 추가
  - 예:
      - 이 디렉터리에 허용되는 파일 종류
      - 금지 의존성
      - 대표 facade/runtime 이름
  - lint/script가 이걸 읽고 차단

  4. shim을 re-export-only로 강제

  - legacy shim 파일 안에 로직 추가를 금지
  - 즉 old path는 오직 export * from ...만 허용
  - 그러면 LLM이 그 파일을 확장 기점으로 쓰기 어려워짐

  5. 파일 헤더 계약

  - 큰 facade/runtime 파일 상단에 짧게 박아둠
  - 예:
      - Facade only
      - Do not add business logic here
      - New runtime code belongs in src/services/photo/*
  - lost in the middle를 줄이려면 파일 바로 위에 있어야 함

  6. 유사도 기반 중복 검사

  - 새 파일 생성/수정 시
      - 함수명
      - 클래스명
      - 파일명
      - export 이름
        이 기존 것과 비슷하면 차단 또는 강한 경고
  - 이건 warning보다 pre-commit fail에 가깝게 운용 가능

  7. entrypoint 고정

  - 새 구현은 반드시 기존 facade를 통해서만 노출
  - 직접 새 runtime을 app entry에서 import 못 하게 함
  - 즉 생성은 해도 공개 surface를 마음대로 늘릴 수 없게 함

  8. ownership map

  - 디렉터리별 책임 소유자를 코드 옆에 둠
  - 예:
      - src/services/photo/ = photo runtime only
      - src/components/home/ = home composition only
  - 새 파일이 ownership에 안 맞으면 차단

  9. template 강제

  - 새 파일은 빈 파일 생성 금지
  - 반드시 템플릿으로 생성
  - 템플릿에 질문이 들어감:
      - 기존 파일은 무엇인가
      - 왜 수정이 아니라 신규인가
      - facade/runtime/helper 중 무엇인가

  10. new-file allowlist

  - 특정 디렉터리는 새 파일 추가 자체를 제한
  - 예:
      - src/components/home/는 승인된 이름 패턴만 허용
      - HomeManager2.js 같은 임의 생성 차단

  핵심 판단

  - handoff/log는 보조 수단입니다
  - lost in the middle가 있으니, 핵심 통제는
      - import 차단
      - 생성 게이트
      - directory contract
      - template 강제
        로 가야 합니다

  실무적으로 제일 효과 큰 조합

  1. no-restricted-imports
  2. legacy shim re-export-only 강제
  3. new module generator
  4. directory contract + structure lint

  한 줄로 말하면:

  - warning보다 강한 해법은 “읽게 하는 것”이 아니라 “잘못 만들 수 없게 하는 것”입니다.

  다음 질문 3/10
  legacy shim은 re-export-only로 강제하고, 로직 추가는 금지할까요?

  - 예
  - 아니오


› 일단 질문 1번부터 10번까지 한 번 다시 뽑아줘


• 좋습니다. legacy 경계를 명확히 하기 위한 폐쇄형 질문 10개를 다시 정리하면 이렇습니다.

  1. legacy shim은 기본적으로 새 코드 import 금지로 두되, 대안이 없고 이유가 기록된 경우에만 예외 허용할까요?

  - 예
  - 아니오

  2. LLM이 새 코드를 만들기 전에 반드시 기존 로직 재사용 / 확장 / 신규 작성 중 하나를 먼저 선언하게 할까요?

  - 예
  - 아니오

  3. legacy shim은 re-export-only로 강제하고, shim 내부에 새 로직 추가는 금지할까요?

  - 예
  - 아니오

  4. 새 파일 생성은 자유 생성 대신 generator/script를 통해서만 허용할까요?

  - 예
  - 아니오

  5. 유사한 이름의 새 파일이나 export가 생기면 warning이 아니라 생성 차단 또는 fail로 올릴까요?

  - 예
  - 아니오

  6. facade 파일에는 Facade only 같은 파일 헤더 계약을 넣고, business logic 추가를 금지할까요?

  - 예
  - 아니오

  7. src/services/** -> src/components/** import 금지 같은 디렉터리 경계를 warning이 아니라 hard rule로 갈까요?

  - 예
  - 아니오

  8. directory contract를 README.md만이 아니라 기계 판독 가능한 규칙 파일까지 둘까요?

  - 예
  - 아니오

  9. new file allowlist를 둬서 특정 디렉터리에는 허용된 이름 패턴의 파일만 추가되게 할까요?

  - 예
  - 아니오

  10. legacy 제거 기준을 “참조 0회 + 대체 경로 안정화 + 일정 기간 경고 없음”으로 명문화할까요?

  - 예
  - 아니오
