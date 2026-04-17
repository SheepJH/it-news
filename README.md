# IT 카드뉴스 자동화

매일 오전 9시, Hacker News 상위 기사를 AI가 한국어 카드뉴스로 변환해 GitHub Pages에 배포하고 Slack으로 알림을 보내는 자동화 파이프라인.

---

## 결과물 예시

- 뷰어: `https://{username}.github.io/it-news/YYYY-MM-DD.html`
- 모바일 가로 스와이프 캐러셀, 하단 핵심 키워드 섹션
- 카드 4~8장 (기사 복잡도에 따라 Claude가 자동 결정)

---

## 파이프라인 전체 흐름

```
[GitHub Actions - 매일 09:00 KST]
        │
        ▼
1. 뉴스 수집 (Hacker News API)
   HN 상위 50개 → 점수순 정렬 → 24시간 이내 + IT 키워드 → 1개 선택
        │
        ▼
2. 카드뉴스 JSON 생성 (Claude Sonnet API)
   기사 제목 + URL → 4~8페이지 구성 결정 → Jinja2 렌더링용 JSON 반환
        │
        ▼
3. PNG 렌더링 (Jinja2 + Playwright)
   JSON → HTML 템플릿 → Headless Chrome → PNG (1080×1080)
        │
        ▼
4. 뷰어 HTML 생성 + GitHub Pages 배포
   캐러셀 뷰어 + 키워드 섹션 → docs/ 커밋 → GitHub Pages 자동 반영
        │
        ▼
5. Slack 알림
   썸네일 + 링크 → Incoming Webhook → DM 수신
```

---

## 비용 분석

### 실제 과금 항목

| 항목 | 비용 | 비고 |
|---|---|---|
| **Claude Sonnet API** | 약 $0.03 / 1회 | 입력 ~2,000토큰 + 출력 ~1,500토큰 |
| 나머지 전부 | **$0** | HN API, GitHub Actions, GitHub Pages, Slack 모두 무료 |

### Claude API 상세 계산

```
claude-sonnet-4-6 기준 (2025년)
  Input:  $3.00 / 1M tokens  →  2,000 tokens = $0.006
  Output: $15.00 / 1M tokens →  1,500 tokens = $0.023
  ──────────────────────────────────────────────────
  1회 합계:                           ≈ $0.03

월간 (30회):   ≈ $0.90
연간 (365회):  ≈ $10.95
$5 충전 시:    ≈ 166회 (약 5.5개월)
```

### GitHub Actions 무료 한도

공개 레포는 무제한 무료. 비공개 레포는 월 2,000분 무료 (1회 실행 약 3~5분 소요).

---

## 각 기술 선택 이유 및 대안

### 1. 뉴스 수집 — Hacker News API

**선택 이유**
- 완전 무료, 인증 불필요
- 커뮤니티 투표로 검증된 기사 (수백~수천 명이 "읽을 만하다"고 올린 것들)
- 점수 기반 정렬로 "오늘 가장 핫한 IT 기사" 자동 선별
- `created_at` 타임스탬프로 24시간 필터 가능

**대안 비교**

| 방식 | 비용 | 품질 | 비고 |
|---|---|---|---|
| **HN API** ✅ | 무료 | 높음 | 커뮤니티 검증 |
| RSS 멀티피드 | 무료 | 중간 | 소스별 편향 가능 |
| NewsAPI | 무료(100req/일) ~ $449/월 | 높음 | 무료 플랜은 24시간 딜레이 |
| Google News RSS | 무료 | 중간 | 비공식, 불안정 |

---

### 2. 카드뉴스 생성 — Claude Sonnet API

**선택 이유**
- 한국어 품질이 GPT-4o와 동등하거나 우수
- 긴 System Prompt + 복잡한 JSON 스키마를 정확히 따름
- Sonnet은 Opus 대비 5배 저렴하면서 구조화 출력 품질 동일

**대안 비교**

| 모델 | 1회 비용 | 한국어 | 구조화 출력 |
|---|---|---|---|
| **Claude Sonnet 4.6** ✅ | ~$0.03 | 우수 | 우수 |
| Claude Opus 4.6 | ~$0.15 | 최고 | 최고 |
| GPT-4o | ~$0.04 | 우수 | 우수 |
| GPT-4o mini | ~$0.005 | 양호 | 양호 |
| Gemini 1.5 Pro | ~$0.02 | 양호 | 양호 |

> 비용을 더 줄이고 싶다면 GPT-4o mini 또는 Gemini Flash 고려 가능. 단 복잡한 JSON 스키마 준수율이 낮아질 수 있음.

---

### 3. 렌더링 — Jinja2 + Playwright

**선택 이유**
- 디자인을 코드(HTML/CSS)로 완전 제어 가능
- 외부 디자인 API 의존 없음 → 비용 $0
- 1080×1080 정확한 픽셀 렌더링 (인스타그램 규격)
- 템플릿 추가/수정이 HTML 파일 하나로 끝남

**대안 비교**

| 방식 | 비용 | 유연성 | 비고 |
|---|---|---|---|
| **Jinja2 + Playwright** ✅ | 무료 | 최고 | 직접 HTML/CSS 작성 |
| Puppeteer | 무료 | 최고 | Node.js 기반 |
| Canva API | $13/월~ | 중간 | 템플릿 제한 |
| html2image | 무료 | 중간 | 품질 낮음 |
| wkhtmltopdf | 무료 | 중간 | CSS 지원 불완전 |

---

### 4. 호스팅 — GitHub Pages

**선택 이유**
- 완전 무료 (공개 레포)
- git push 한 번으로 자동 배포
- URL이 깔끔하고 영구적
- 코드와 결과물을 같은 레포에서 버전 관리

**대안 비교**

| 방식 | 비용 | 편의성 | 비고 |
|---|---|---|---|
| **GitHub Pages** ✅ | 무료 | 높음 | git push = 배포 |
| Vercel | 무료(취미) | 높음 | 더 빠른 CDN |
| Netlify | 무료(취미) | 높음 | 유사 |
| S3 + CloudFront | ~$1/월 | 낮음 | 설정 복잡 |

---

### 5. 스케줄링 — GitHub Actions

**선택 이유**
- 별도 서버 불필요
- cron 표현식으로 정확한 시간 예약
- 실행 로그, 실패 알림 기본 제공
- 이미 GitHub을 쓰므로 추가 비용/설정 없음

**대안 비교**

| 방식 | 비용 | 비고 |
|---|---|---|
| **GitHub Actions** ✅ | 무료 | 서버리스, 공개 레포 무제한 |
| cron + 개인 서버 | 서버비 | 항상 켜져있어야 함 |
| AWS Lambda + EventBridge | ~$0/월 | 설정 복잡 |
| Railway / Render | $5~/월 | 간단하지만 유료 |

---

### 6. 알림 — Slack Incoming Webhook

**선택 이유**
- Webhook URL 하나만 발급하면 끝 (토큰 갱신 없음)
- 모바일 앱 푸시 알림 확실
- 썸네일 이미지 자동 표시
- 버튼 클릭으로 바로 뷰어 이동

**대안 비교**

| 방식 | 설정 난이도 | 푸시 알림 | 비고 |
|---|---|---|---|
| **Slack Webhook** ✅ | 쉬움 | 있음 | 토큰 관리 불필요 |
| Telegram Bot | 쉬움 | 있음 | 개인용으로 추천 대안 |
| Discord Webhook | 쉬움 | 있음 | 게이머 친화적 |
| 카카오 나에게 보내기 | 어려움 | 없음 | 토큰 만료 관리 필요 |
| 이메일 (Gmail SMTP) | 중간 | 없음 | 실시간성 낮음 |

---

## 파일 구조

```
it-news/
├── .github/
│   └── workflows/
│       └── daily-news.yml       # GitHub Actions 스케줄러
├── design/
│   └── templates/               # Jinja2 HTML 템플릿 (1080×1080)
│       ├── explainer_01_cover.html
│       ├── explainer_02_definition.html
│       ├── explainer_03_comparison.html
│       ├── explainer_04_process.html
│       ├── explainer_05_example.html
│       ├── explainer_06_conclusion.html
│       ├── explainer_stats.html
│       ├── explainer_timeline.html
│       ├── explainer_faq.html
│       └── explainer_quote.html
├── docs/                        # GitHub Pages 서빙 디렉토리
│   ├── index.html               # 날짜별 썸네일 그리드
│   ├── YYYY-MM-DD.html          # 스와이프 뷰어
│   └── YYYY-MM-DD/
│       ├── card_01.png
│       └── card_N.png
├── scripts/
│   ├── main.py                  # 진입점, 파이프라인 오케스트레이션
│   ├── fetch_news.py            # HN API 뉴스 수집
│   ├── claude_processor.py      # Claude API JSON 생성
│   ├── renderer.py              # HTML → PNG 렌더링, 뷰어 생성
│   ├── slack_notify.py          # Slack 알림
│   └── test_render.py           # 로컬 테스트 (API 비용 없이 렌더링 확인)
├── requirements.txt
└── .env.example
```

---

## 템플릿 종류 (8종)

Claude가 기사 내용에 따라 4~8장을 자유 조합.

| 템플릿 | 용도 | 핵심 변수 |
|---|---|---|
| `explainer_01_cover` | 표지 (항상 1페이지) | question, subtitle, date |
| `explainer_02_definition` | 핵심 개념 정의 | headline, body_text |
| `explainer_03_comparison` | Before / After 비교 | before_items, after_chain |
| `explainer_04_process` | 단계별 작동 원리 | steps[{title, desc}] |
| `explainer_05_example` | 실제 사례 | items[{title, desc, tag}] |
| `explainer_06_conclusion` | 한 줄 요약 (항상 마지막) | headline_parts, body_text |
| `explainer_stats` | 핵심 수치/통계 | stats[{value, label, note}] |
| `explainer_timeline` | 연대기/흐름 | events[{date, event}] |
| `explainer_faq` | Q&A | faqs[{q, a}] |
| `explainer_quote` | 주요 인용구 | quote, source, context |

---

## 설치 및 실행

### 로컬 테스트 (API 비용 없음)

```bash
pip install -r requirements.txt
playwright install chromium

cd scripts
python test_render.py
open ../docs/_test.html
```

### 전체 파이프라인 실행

```bash
# .env 파일 작성
cp .env.example .env
# ANTHROPIC_API_KEY 입력

cd scripts
python main.py
```

---

## GitHub Actions 설정

### 필요한 Secrets

| Secret | 설명 |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic Console에서 발급 |
| `SLACK_WEBHOOK_URL` | Slack 앱 → Incoming Webhooks |
| `GH_REPO` | `username/it-news` 형식 |

### 실행 시간 변경

`.github/workflows/daily-news.yml`에서 cron 수정:

```yaml
- cron: '0 0 * * *'   # UTC 00:00 = KST 09:00
- cron: '0 22 * * *'  # UTC 22:00 = KST 07:00
```
