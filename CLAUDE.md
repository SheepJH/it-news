# IT 카드뉴스 자동화 — Claude 작업 지침

## ⚠️ 작업 시작 전 필독

템플릿/디자인 관련 작업 시 반드시:
1. `design/DESIGN_SPEC.md` 먼저 읽기
2. 새 작업 시 스펙을 **기준**으로 삼기
3. 코드를 먼저 수정했다면 → 스펙도 함께 업데이트 (코드 = 최종 진실)

---

## 프로젝트 목적

매일 KST 09:00, Hacker News 상위 기사를 Claude가 한국어 카드뉴스로 변환해
GitHub Pages에 배포하고 Slack으로 알림을 보내는 자동화 파이프라인.
개인 사용 목적 — 내가 매일 IT 뉴스를 빠르게 소비하기 위한 도구.

## 파이프라인

```
HN API (상위 50개 병렬 조회)
  → 점수순 정렬 + 24h 필터 + IT 키워드 필터 + 중복 제거 (used_urls.json)
  → Claude Sonnet 4.6 → 카드뉴스 JSON (4~8페이지)
  → Jinja2 → Playwright → 1080×1080 PNG × N장
  → docs/ 커밋 → GitHub Pages 배포
  → Slack Webhook 알림
```

실행: `.github/workflows/daily-news.yml` cron `0 0 * * *` (UTC 00:00 = KST 09:00)

---

## 파일 역할

| 파일 | 역할 |
|---|---|
| `scripts/main.py` | 파이프라인 오케스트레이션 |
| `scripts/fetch_news.py` | HN API 뉴스 수집 + 필터링 |
| `scripts/claude_processor.py` | Claude API 카드뉴스 JSON 생성 |
| `scripts/renderer.py` | HTML → PNG, 뷰어/인덱스 HTML 생성 |
| `scripts/slack_notify.py` | Slack Webhook 알림 |
| `scripts/test_render.py` | 로컬 테스트 (API 비용 없음, 목 데이터) |
| `design/templates/` | Jinja2 HTML 템플릿 (1080×1080) |
| `design/DESIGN_SPEC.md` | 디자인 스펙 (Source of Truth) |
| `docs/` | GitHub Pages 루트 |
| `docs/used_urls.json` | 중복 기사 방지 URL 기록 |

---

## 코딩 규칙

- **Python 3.9 호환** — `dict | None` 타입 힌트 사용 불가 (힌트 생략 또는 `Optional[dict]`)
- **환경변수**: `ANTHROPIC_API_KEY`, `SLACK_WEBHOOK_URL`, `GH_REPO`
- `docs/` 변경 후 반드시 git commit + push 해야 GitHub Pages에 반영

---

## CLAUDE.md 자체 업데이트 규칙

아래 항목이 변경되면 **이 파일(CLAUDE.md)도 함께 수정**한다.

- 파이프라인 단계 추가/변경/삭제 → `## 파이프라인` 섹션 수정
- 스크립트 파일 추가/삭제/역할 변경 → `## 파일 역할` 표 수정
- 환경변수 추가/삭제 → `## 코딩 규칙` 수정
- cron 시간 변경 → `## 파이프라인` 실행 시간 수정

---

## README 동기화 규칙

아래 파일 수정 시 **README.md 해당 섹션도 함께 업데이트**한다.

| 수정 파일 | README 업데이트 대상 |
|---|---|
| `scripts/fetch_news.py` | 🔄 파이프라인 흐름 1단계, 🛠 기술 선택 이유 (뉴스 수집) |
| `scripts/claude_processor.py` | 🔄 파이프라인 흐름 2단계, 💰 비용 분석, 🛠 기술 선택 이유 (AI 생성) |
| `scripts/renderer.py` | 🔄 파이프라인 흐름 3~4단계, 🛠 기술 선택 이유 (렌더링) |
| `scripts/slack_notify.py` | 🔄 파이프라인 흐름 5단계, 🛠 기술 선택 이유 (알림) |
| `scripts/main.py` | 🔄 파이프라인 흐름 전체 |
| `design/templates/` 추가/삭제 | 🎨 템플릿 종류 표 |
| `design/DESIGN_SPEC.md` | 🎨 템플릿 종류 표 |
| `.github/workflows/daily-news.yml` | ⚙️ GitHub Actions 설정 섹션 |
| `requirements.txt` | 🚀 설치 및 실행 섹션 |
