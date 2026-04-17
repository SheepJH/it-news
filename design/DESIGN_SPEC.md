# 카드뉴스 디자인 스펙

> 이 문서는 **Source of Truth** 입니다.
> 코드와 이 문서가 다르면, 코드를 수정하세요.

---

## 공통 규칙 (모든 템플릿)

### 캔버스
- **크기**: 1080 × 1080 px
- **padding**: 90px (기본) / 80px (comparison, process, example)

### 타이포그래피
- **폰트**: Pretendard 웹폰트
  (`https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css`)
- **허용 weight**: 400 (regular), 500 (medium) 만
- **금지**: weight 600/700, 이탤릭
- **예외**: quote 템플릿의 따옴표 장식만 Georgia serif 허용

### 컬러 팔레트

| 용도 | HEX |
|---|---|
| 카드 배경 (기본) | `#FFFFFF` |
| body 배경 | `#FAFAFA` |
| 카드 테두리 | `#E8E8E8` (1px solid) |
| 텍스트 주요 | `#111111` |
| 텍스트 보조 | `#555555` |
| 텍스트 메타 | `#777777` |
| 텍스트 라벨 | `#999999` |
| 포인트 (형광) | `#FFE566` |
| 긍정/After 텍스트 | `#2D7A3E` |
| 긍정/After 배경 | `#F0F7F0` |
| 부정/Before 텍스트 | `#C44536` |
| 리스트 아이템 배경 | `#FAFAFA` |
| 태그 LIVE | `#2D7A3E` / `#F0F7F0` |
| 태그 NEW | `#BA7517` / `#FAEEDA` |

### 공통 레이아웃 요소
- **좌상단**: `section_label` — 24px, #999, letter-spacing 2px, weight 500
- **우상단**: 페이지 번호 — `02 / 06` 형식, 22px, #999
- **구분선 (일부 템플릿)**: `80px × 4px`, #111 (definition) 또는 #FFE566 (conclusion)

### 금지 사항
- ❌ 이모지
- ❌ 그라데이션 배경
- ❌ drop-shadow (box-shadow)
- ❌ @핸들 표기
- ❌ "다음 편", "저장·팔로우" CTA
- ❌ 원문 기사 문장 그대로 복붙

---

## 템플릿별 스펙

### explainer_01_cover.html
**변수**: `question`, `subtitle`, `date`
**padding**: 90px

- 배경: `#FFFFFF`
- 상단: `EXPLAINER` 태그 (22px, weight 500, 검정 배경 흰 텍스트, padding 10×24, border-radius 6px, letter-spacing 2px)
- 날짜: 22px, #BBB, margin-top 10px
- Q. 라벨: 30px, #CCC, margin-bottom 18px
- 질문: 88px, weight 500, #111, line-height 1.2, letter-spacing -0.03em, white-space pre-line
- 부제목: 30px, #666, margin-top 40px, line-height 1.55
- 하단: `SWIPE →` 22px, #111, weight 500

**글자 수 제한**:
- `question`: 최대 3줄, 줄당 7자 이하, `\n`으로 줄바꿈
- `subtitle`: 최대 2줄, 줄당 20자 이하

---

### explainer_02_definition.html
**변수**: `section_label`, `page_current`, `page_total`, `label_top`, `headline_before_highlight`, `headline_highlight`, `body_text`
**padding**: 90px

- `label_top`: 26px, #999, letter-spacing 2px, weight 500, margin-bottom 28px
- 헤드라인: 70px, weight 500, #111, line-height 1.35, letter-spacing -0.02em
- 형광펜: `background: linear-gradient(transparent 60%, #FFE566 60%); padding: 0 6px`
- 구분선: `80px × 4px`, #111, margin 50px 0
- 본문: 34px, #555, line-height 1.6, white-space pre-line

**글자 수 제한**:
- `headline_before_highlight + headline_highlight`: 각 줄 10자 이하
- `body_text`: 최대 3줄, 줄당 15자 이하

---

### explainer_03_comparison.html
**변수**: `section_label`, `page_current`, `page_total`, `headline`, `before_label`, `before_items`, `before_note`, `after_label`, `after_chain`, `after_note`
**padding**: 80px | layout: `flex-start; gap: 60px`

- 헤드라인: 46px, weight 500, #111, letter-spacing -0.02em, margin-bottom 40px
- Before 박스: `#FAFAFA` 배경, border-radius 20px, padding 36×40
- After 박스: `#F0F7F0` 배경, border-radius 20px, padding 36×40
- 박스 라벨: 22px, weight 500, letter-spacing 2px, margin-bottom 18px
  - Before 라벨: `#C44536`
  - After 라벨: `#2D7A3E`
- chip: 흰 배경 + `#E0E0E0` 테두리, padding 10×18, border-radius 8px, 26px, #555
- chip-highlight (after 2번째): `#2D7A3E` 배경 흰 텍스트
- 화살표: before `↔` #C44536 / after `→` #2D7A3E, 24px
- note: 22px, before #999 / after #2D7A3E

**글자 수 제한**:
- `before_items`: 각 10자 이하, 최대 4개
- `after_chain`: 각 10자 이하, 최대 3개

---

### explainer_04_process.html
**변수**: `section_label`, `page_current`, `page_total`, `headline`, `steps[{title, desc}]`
**padding**: 80px

- 헤드라인: 48px, weight 500, #111, letter-spacing -0.02em, margin-bottom 60px
- steps: flex column, gap 40px
- 번호 배지: `72×72px` 원형, 검정 배경 흰 텍스트, 30px weight 500
- step-title: 38px, weight 500, #111, letter-spacing -0.01em, margin-bottom 8px
- step-desc: 28px, #777, line-height 1.5

**글자 수 제한**:
- `steps.title`: 12자 이하
- `steps.desc`: 20자 이하

---

### explainer_05_example.html
**변수**: `section_label`, `page_current`, `page_total`, `headline`, `items[{title, desc, tag}]`
**padding**: 80px

- 헤드라인: 48px, weight 500, #111, letter-spacing -0.02em, margin-bottom 46px
- 아이템: `#FAFAFA` 배경, **border-radius 16px**, padding 30×36, gap 20px
- item-title: 32px, weight 500, #111, margin-bottom 6px
- item-desc: 24px, #777
- 태그: 22px, weight 500, padding 8×18, border-radius 8px, letter-spacing 1px
  - LIVE: #2D7A3E / #F0F7F0
  - NEW: #BA7517 / #FAEEDA

**글자 수 제한**:
- `items.title`: 15자 이하
- `items.desc`: 20자 이하

---

### explainer_stats.html
**변수**: `section_label`, `page_current`, `page_total`, `headline`, `stats[{value, label, note}]`
**padding**: 90px

- 헤드라인: 48px, weight 500, #111, letter-spacing -0.02em, margin-bottom 70px
- stats: flex row, justify space-between, gap 32px
- 각 stat: 상단 `border-top: 4px solid #FFE566`, padding-top 36px
- stat-value: **80px**, weight 500, #111, letter-spacing -0.04em, line-height 1
- stat-label: 28px, weight 500, #111, margin-bottom 10px
- stat-note: 22px, #999, line-height 1.4

**글자 수 제한**:
- `stats.value`: 8자 이하 (숫자/퍼센트)
- `stats.label`: 12자 이하
- `stats.note`: 20자 이하

---

### explainer_timeline.html
**변수**: `section_label`, `page_current`, `page_total`, `headline`, `events[{date, event}]`
**padding**: 90px

- 헤드라인: 48px, weight 500, #111, letter-spacing -0.02em, margin-bottom 56px
- event: flex row, gap 40px, padding-bottom 40px
- 세로 연결선: `left: 168px`, 2px, #E8E8E8 (마지막 항목 제외 `::before`)
- event-date: min-width 130px, 22px, #999, text-align right
- event-dot: 16×16px 원형, **#FFE566** 배경
- event-text: 32px, weight 500, #111, line-height 1.4

**글자 수 제한**:
- `events.date`: 10자 이하
- `events.event`: 20자 이하

---

### explainer_faq.html
**변수**: `section_label`, `page_current`, `page_total`, `headline`, `faqs[{q, a}]`
**padding**: 90px

- 헤드라인: 48px, weight 500, #111, letter-spacing -0.02em, margin-bottom 56px
- faq-item: **border-left: 4px solid #FFE566**, padding-left 32px, gap 36px
- Q. 라벨: 28px, weight 500, **#FFE566**
- 질문 텍스트: 32px, weight 500, #111, line-height 1.35
- 답변 텍스트: 28px, #555, line-height 1.5, padding-left 42px

**글자 수 제한**:
- `faqs.q`: 20자 이하
- `faqs.a`: 30자 이하

---

### explainer_quote.html
**변수**: `section_label`, `page_current`, `page_total`, `quote`, `source`, `context`
**padding**: 90px

- 따옴표 장식: 120px, **Georgia serif** (유일한 serif 예외), #FFE566, line-height 0.6, margin-bottom 32px
- 인용구: 58px, weight 500, #111, line-height 1.4, letter-spacing -0.02em, white-space pre-line
- 구분선: `60px × 3px`, #FFE566, margin-bottom 28px
- 출처: 28px, weight 500, #111, margin-bottom 12px
- 맥락: 24px, #999
- `context`는 optional (`{% if context %}`)

**글자 수 제한**:
- `quote`: 2줄, 줄당 20자 이하, `\n`으로 줄바꿈
- `source`: 20자 이하
- `context`: 30자 이하

---

### explainer_06_conclusion.html
**변수**: `section_label`, `page_current`, `page_total`, `label_top`, `headline_parts[{text, highlight}]`, `body_text`
**padding**: 90px

- 배경: **`#111111`** (유일한 다크 배경)
- section_label: **#FFE566** (다른 템플릿과 달리 노란색)
- page-num: **#666** (다른 템플릿과 달리 #666)
- `label_top`: 26px, **#666**, letter-spacing 2px, weight 500, margin-bottom 28px
- 헤드라인: **68px**, weight 500, 흰색, line-height 1.35, letter-spacing -0.02em
- `highlight: true` 파트: **#FFE566** (`<span class="accent">`)
- 각 part는 `<br/>` 로 줄바꿈
- 구분선: `80px × 4px`, **#FFE566**, margin 50px 0
- 본문: 30px, **#AAA**, line-height 1.6, white-space pre-line

**글자 수 제한**:
- `headline_parts`: 각 `part.text` 8자 이하, 최대 4개

---

## 새 템플릿 추가 체크리스트

1. 이 문서에 스펙 섹션 추가
2. `design/templates/`에 HTML 파일 추가 (네이밍: `explainer_{역할}.html`)
3. `scripts/claude_processor.py` SYSTEM_PROMPT에 JSON 스키마 추가
4. `scripts/test_render.py` MOCK_DATA에 샘플 데이터 추가
5. `README.md` 🎨 템플릿 종류 표 업데이트
