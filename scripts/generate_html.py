from datetime import datetime, timedelta

# ── 디자인 토큰 ───────────────────────────────────────────────────────────────
CSS = """
:root {
  --accent:       #7C3AED;
  --accent-mid:   #6D28D9;
  --accent-light: #EDE9FE;
  --accent-xlight:#F5F3FF;
  --text-1:       #111827;
  --text-2:       #374151;
  --text-3:       #6B7280;
  --text-4:       #9CA3AF;
  --bg:           #F0EEFF;
  --card:         #FFFFFF;
  --border:       #E5E7EB;
  --radius:       20px;
  --shadow:       0 4px 28px rgba(109,40,217,.10);
}

* { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
               'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
  background: var(--bg);
  color: var(--text-1);
  min-height: 100vh;
  padding-bottom: 60px;
}

/* ── 페이지 헤더 ── */
.page-header {
  text-align: center;
  padding: 48px 20px 28px;
}
.site-label {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--accent);
  background: var(--accent-light);
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 14px;
}
.page-date {
  font-size: 36px;
  font-weight: 900;
  color: var(--text-1);
  line-height: 1;
  letter-spacing: -.02em;
}
.page-sub {
  margin-top: 8px;
  font-size: 14px;
  color: var(--text-3);
}

/* ── 그리드 ── */
.grid {
  max-width: 1040px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}
@media (max-width: 660px) {
  .grid { grid-template-columns: 1fr; }
}
.card-full { grid-column: 1 / -1; }

/* ── 카드 공통 ── */
.card {
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.card-accent-bar {
  height: 4px;
  background: linear-gradient(90deg, var(--accent) 0%, #A78BFA 100%);
}
.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px 0;
}
.badge {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .06em;
  color: var(--accent);
  background: var(--accent-light);
  padding: 3px 10px;
  border-radius: 20px;
}
.card-num {
  font-size: 12px;
  color: var(--text-4);
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}

/* ── 카드 본문 ── */
.card-body {
  padding: 16px 20px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.card-title {
  font-size: 21px;
  font-weight: 800;
  line-height: 1.35;
  color: var(--text-1);
  word-break: keep-all;
}
.card-subtitle {
  font-size: 13px;
  color: var(--accent);
  font-weight: 600;
  margin-top: -8px;
}
.divider {
  border: none;
  border-top: 1px solid var(--border);
}

/* 요약 */
.summary-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .08em;
  color: var(--text-3);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.summary-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.summary-list li {
  font-size: 14px;
  color: var(--text-2);
  line-height: 1.55;
  padding-left: 18px;
  position: relative;
}
.summary-list li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--accent);
  font-size: 12px;
  top: 2px;
}

/* 왜 중요한가 박스 */
.insight-box {
  background: var(--accent-light);
  border-radius: 12px;
  padding: 13px 15px;
}
.insight-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .1em;
  color: var(--accent);
  text-transform: uppercase;
  display: block;
  margin-bottom: 5px;
}
.insight-text {
  font-size: 13px;
  color: var(--text-1);
  line-height: 1.6;
  word-break: keep-all;
}

/* ── 오늘의 키워드 섹션 ── */
.kw-section {
  max-width: 1040px;
  margin: 0 auto;
  padding: 0 20px;
}
.kw-section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}
.kw-section-title {
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .1em;
  color: var(--accent);
  text-transform: uppercase;
}
.kw-section-line {
  flex: 1;
  height: 1px;
  background: var(--accent-light);
}
.kw-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
@media (max-width: 660px) {
  .kw-list { grid-template-columns: 1fr; }
}
.kw-item {
  background: var(--card);
  border-radius: 14px;
  padding: 16px 18px;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.kw-term {
  font-size: 18px;
  font-weight: 900;
  color: var(--accent);
  line-height: 1;
}
.kw-full {
  font-size: 11px;
  color: var(--text-4);
  font-weight: 500;
}
.kw-desc {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.6;
  word-break: keep-all;
}

/* 카드 푸터 */
.card-footer {
  border-top: 1px solid var(--border);
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}
.source-link {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
  transition: color .15s;
}
.source-link:hover { color: var(--accent-mid); }
.source-meta {
  font-size: 12px;
  color: var(--text-4);
}

/* ── Versus 카드 ── */
.vs-grid {
  display: grid;
  grid-template-columns: 1fr 28px 1fr;
  gap: 8px;
  align-items: start;
}
.vs-col {
  background: var(--accent-xlight);
  border-radius: 12px;
  padding: 12px;
}
.vs-name {
  font-size: 13px;
  font-weight: 800;
  color: var(--text-1);
  text-align: center;
  margin-bottom: 8px;
  word-break: keep-all;
}
.vs-sep {
  font-size: 13px;
  font-weight: 900;
  color: var(--accent);
  text-align: center;
  padding-top: 14px;
}
.vs-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.vs-list li {
  font-size: 12px;
  line-height: 1.4;
  color: var(--text-2);
}
.vs-spec {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  margin-top: 6px;
  text-align: center;
}
.verdict {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-mid) 100%);
  border-radius: 12px;
  padding: 12px 15px;
  color: white;
}
.verdict-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .1em;
  opacity: .75;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.verdict-text {
  font-size: 14px;
  font-weight: 700;
  line-height: 1.4;
}

/* ── Data 카드 ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.stat-box {
  background: var(--accent-xlight);
  border-radius: 12px;
  padding: 14px 10px;
  text-align: center;
}
.stat-value {
  font-size: 22px;
  font-weight: 900;
  color: var(--accent);
  line-height: 1;
}
.stat-unit {
  font-size: 11px;
  color: var(--accent);
  font-weight: 600;
}
.stat-label {
  font-size: 11px;
  color: var(--text-3);
  margin-top: 5px;
  line-height: 1.3;
}

/* ── Timeline 카드 ── */
.timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.tl-item {
  display: grid;
  grid-template-columns: 56px 1px 1fr;
  gap: 0 12px;
  position: relative;
}
.tl-date {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  text-align: right;
  padding: 2px 0 16px;
  line-height: 1.2;
}
.tl-line-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.tl-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--accent);
  flex-shrink: 0;
  margin-top: 3px;
}
.tl-line {
  flex: 1;
  width: 2px;
  background: var(--accent-light);
  min-height: 14px;
}
.tl-event {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.5;
  padding-bottom: 16px;
}
.tl-event.current {
  font-weight: 700;
  color: var(--text-1);
}
.tl-item:last-child .tl-line { display: none; }

/* ── Explainer 카드 ── */
.one-liner {
  background: linear-gradient(135deg, var(--accent) 0%, #A78BFA 100%);
  border-radius: 12px;
  padding: 16px;
  color: white;
  text-align: center;
}
.one-liner-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .1em;
  opacity: .75;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.one-liner-text {
  font-size: 15px;
  font-weight: 800;
  line-height: 1.4;
}

/* ── 내비게이션 ── */
.nav-bar {
  max-width: 1040px;
  margin: 28px auto 0;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
}
.nav-btn {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
  background: var(--card);
  border-radius: 10px;
  padding: 9px 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
  transition: background .15s;
}
.nav-btn:hover { background: var(--accent-light); }
.nav-btn.disabled {
  color: var(--text-4);
  pointer-events: none;
  box-shadow: none;
}
"""


# ── 카드 렌더러 ─────────────────────────────────────────────────────────────

def _summary_html(summary):
    items = "".join(f"<li>{s}</li>" for s in summary)
    return f"""
      <div>
        <p class="summary-label">📌 핵심 요약</p>
        <ul class="summary-list">{items}</ul>
      </div>"""

def _insight_html(importance):
    return f"""
      <div class="insight-box">
        <span class="insight-label">💡 왜 중요한가</span>
        <p class="insight-text">{importance}</p>
      </div>"""

def _footer_html(url, score, comments):
    return f"""
    <div class="card-footer">
      <a class="source-link" href="{url}" target="_blank">원문 보기 →</a>
      <span class="source-meta">⬆ {score} &nbsp;💬 {comments}</span>
    </div>"""

def _card_wrap(inner, full_width=False):
    cls = "card card-full" if full_width else "card"
    return f'<article class="{cls}"><div class="card-accent-bar"></div>{inner}</article>'


def render_standard(c, idx, total):
    subtitle = f'<p class="card-subtitle">{c["subtitle_ko"]}</p>' if c.get("subtitle_ko") else ""
    inner = f"""
    <div class="card-meta">
      <span class="badge">{c['category']}</span>
      <span class="card-num">{idx:02d} / {total:02d}</span>
    </div>
    <div class="card-body">
      <h2 class="card-title">{c['title_ko']}</h2>
      {subtitle}
      <hr class="divider">
      {_summary_html(c['summary'])}
      {_insight_html(c['importance'])}
    </div>
    {_footer_html(c['url'], c['score'], c['comments'])}"""
    return _card_wrap(inner)


def render_versus(c, idx, total):
    v = c.get("versus") or {}
    a, b = v.get("a", {}), v.get("b", {})

    def col(side):
        pros = "".join(f"<li>✅ {p}</li>" for p in side.get("pros", []))
        cons = "".join(f"<li>❌ {p}</li>" for p in side.get("cons", []))
        spec = f'<p class="vs-spec">{side["spec"]}</p>' if side.get("spec") else ""
        return f"""
        <div class="vs-col">
          <p class="vs-name">{side.get('name','')}</p>
          <ul class="vs-list">{pros}{cons}</ul>
          {spec}
        </div>"""

    inner = f"""
    <div class="card-meta">
      <span class="badge">비교 분석</span>
      <span class="card-num">{idx:02d} / {total:02d}</span>
    </div>
    <div class="card-body">
      <h2 class="card-title">{c['title_ko']}</h2>
      <hr class="divider">
      <div class="vs-grid">
        {col(a)}
        <div class="vs-sep">VS</div>
        {col(b)}
      </div>
      <div class="verdict">
        <p class="verdict-label">🏆 결론</p>
        <p class="verdict-text">{v.get('verdict','')}</p>
      </div>
    </div>
    {_footer_html(c['url'], c['score'], c['comments'])}"""
    return _card_wrap(inner)


def render_data(c, idx, total):
    stats = c.get("stats") or []
    stat_boxes = ""
    for s in stats[:3]:
        stat_boxes += f"""
        <div class="stat-box">
          <p class="stat-value">{s.get('value','')}<span class="stat-unit">{s.get('unit','')}</span></p>
          <p class="stat-label">{s.get('label','')}</p>
        </div>"""

    inner = f"""
    <div class="card-meta">
      <span class="badge">{c['category']}</span>
      <span class="card-num">{idx:02d} / {total:02d}</span>
    </div>
    <div class="card-body">
      <h2 class="card-title">{c['title_ko']}</h2>
      <hr class="divider">
      {'<div class="stats-grid">' + stat_boxes + '</div>' if stat_boxes else ''}
      {_summary_html(c['summary'])}
      {_insight_html(c['importance'])}
    </div>
    {_footer_html(c['url'], c['score'], c['comments'])}"""
    return _card_wrap(inner)


def render_timeline(c, idx, total):
    tl = c.get("timeline") or []
    tl_html = ""
    for i, t in enumerate(tl):
        is_last = i == len(tl) - 1
        event_cls = "tl-event current" if is_last else "tl-event"
        tl_html += f"""
        <div class="tl-item">
          <p class="tl-date">{t.get('date','')}</p>
          <div class="tl-line-wrap">
            <div class="tl-dot"></div>
            <div class="tl-line"></div>
          </div>
          <p class="{event_cls}">{t.get('event','')}</p>
        </div>"""

    inner = f"""
    <div class="card-meta">
      <span class="badge">{c['category']}</span>
      <span class="card-num">{idx:02d} / {total:02d}</span>
    </div>
    <div class="card-body">
      <h2 class="card-title">{c['title_ko']}</h2>
      <hr class="divider">
      {'<div class="timeline">' + tl_html + '</div>' if tl_html else _summary_html(c['summary'])}
      {_insight_html(c['importance'])}
    </div>
    {_footer_html(c['url'], c['score'], c['comments'])}"""
    return _card_wrap(inner)


def render_explainer(c, idx, total):
    subtitle = c.get("subtitle_ko", "")
    one_liner = f"""
      <div class="one-liner">
        <p class="one-liner-label">한 줄 정리</p>
        <p class="one-liner-text">{subtitle}</p>
      </div>""" if subtitle else ""

    inner = f"""
    <div class="card-meta">
      <span class="badge">💡 개념 설명</span>
      <span class="card-num">{idx:02d} / {total:02d}</span>
    </div>
    <div class="card-body">
      <h2 class="card-title">{c['title_ko']}</h2>
      <hr class="divider">
      {one_liner}
      {_summary_html(c['summary'])}
      {_insight_html(c['importance'])}
    </div>
    {_footer_html(c['url'], c['score'], c['comments'])}"""
    return _card_wrap(inner)


RENDERERS = {
    "versus":    render_versus,
    "data":      render_data,
    "timeline":  render_timeline,
    "explainer": render_explainer,
}


def render_keywords_section(keywords):
    """오늘의 키워드 섹션 HTML 생성"""
    if not keywords:
        return ""

    items_html = ""
    for kw in keywords:
        full = f'<p class="kw-full">{kw["full"]}</p>' if kw.get("full") else ""
        items_html += f"""
        <div class="kw-item">
          <p class="kw-term">{kw['term']}</p>
          {full}
          <p class="kw-desc">{kw['desc']}</p>
        </div>"""

    return f"""
  <section class="kw-section">
    <div class="kw-section-header">
      <span class="kw-section-title">오늘의 키워드</span>
      <div class="kw-section-line"></div>
    </div>
    <div class="kw-list">{items_html}</div>
  </section>"""


# ── 페이지 생성 ───────────────────────────────────────────────────────────────

def generate_page(cards, date_str, keywords=None, prev_date=None, next_date=None):
    """카드 목록으로 전체 HTML 페이지 생성"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    date_display = dt.strftime("%Y년 %m월 %d일")
    dow = ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]

    total = len(cards)
    cards_html = ""
    for i, card in enumerate(cards, 1):
        renderer = RENDERERS.get(card.get("type", "standard"), render_standard)
        cards_html += renderer(card, i, total)

    kw_section = render_keywords_section(keywords or [])

    prev_link = f'<a class="nav-btn" href="{prev_date}.html">← {prev_date}</a>' if prev_date else '<span class="nav-btn disabled">← 이전</span>'
    next_link = f'<a class="nav-btn" href="{next_date}.html">{next_date} →</a>' if next_date else '<span class="nav-btn disabled">다음 →</span>'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IT 카드뉴스 — {date_display}</title>
  <style>{CSS}</style>
</head>
<body>

  <header class="page-header">
    <p class="site-label">IT 카드뉴스</p>
    <h1 class="page-date">{date_display} ({dow})</h1>
    <p class="page-sub">오늘의 IT 핵심 뉴스 {total}선</p>
  </header>

  <div class="grid">
    {cards_html}
  </div>

  {kw_section}

  <nav class="nav-bar">
    {prev_link}
    {next_link}
  </nav>

</body>
</html>"""


def generate_index(dates):
    """아카이브 인덱스 페이지 생성"""
    items = ""
    for d in sorted(dates, reverse=True):
        dt = datetime.strptime(d, "%Y-%m-%d")
        label = dt.strftime("%Y.%m.%d")
        dow = ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]
        items += f'<a class="idx-item" href="{d}.html"><span class="idx-date">{label}</span><span class="idx-dow">{dow}요일</span></a>\n'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IT 카드뉴스 아카이브</title>
  <style>
    {CSS}
    .idx-grid {{
      max-width: 480px;
      margin: 0 auto;
      padding: 0 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .idx-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--card);
      border-radius: 14px;
      padding: 16px 20px;
      text-decoration: none;
      box-shadow: var(--shadow);
      transition: background .15s;
    }}
    .idx-item:hover {{ background: var(--accent-light); }}
    .idx-date {{ font-size: 18px; font-weight: 800; color: var(--text-1); }}
    .idx-dow  {{ font-size: 13px; color: var(--accent); font-weight: 600; }}
  </style>
</head>
<body>
  <header class="page-header">
    <p class="site-label">IT 카드뉴스</p>
    <h1 class="page-date">아카이브</h1>
    <p class="page-sub">지난 뉴스 모아보기</p>
  </header>
  <div class="idx-grid">{items}</div>
</body>
</html>"""
