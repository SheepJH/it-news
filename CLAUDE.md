# IT 카드뉴스 자동화

매일 KST 09:00 Hacker News → Claude 요약 → 1080×1080 PNG 카드뉴스 → GitHub Pages + Slack.

## 작업 시 원칙
- **Python 3.9 호환**: `dict | None` X, `Optional[dict]` O
- **디자인 작업 전**: `design/DESIGN_SPEC.md` 먼저 읽기. 코드와 스펙이 다르면 코드가 진실, 스펙을 맞춰 수정.
- **코드 변경 시**: 영향받는 문서(README, DESIGN_SPEC, 이 파일)도 함께 갱신.
- **`docs/` 수정 후**: commit + push 필수 (Pages 반영).

## 환경변수
`ANTHROPIC_API_KEY`, `SLACK_WEBHOOK_URL`, `GH_REPO`

## 구조
- `scripts/` — 파이프라인 (main → fetch_news → claude_processor → renderer → slack_notify)
- `design/` — 템플릿(Jinja2) + 스펙
- `docs/` — Pages 루트, `used_urls.json`으로 중복 방지
- `.github/workflows/daily-news.yml` — cron `0 0 * * *` (UTC 00:00 = KST 09:00)
