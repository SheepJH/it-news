import json
from datetime import datetime

CAT_EMOJI = {
    "AI/ML": "🤖", "보안": "🔐", "개발": "💻",
    "비즈니스": "📈", "기타": "📰",
}

def card_to_js(card):
    cat = card.get("category", "기타")
    t   = card.get("type", "standard")

    if t == "versus":
        v = card.get("versus") or {}
        slides = [
            {"type": "versus", "a": v.get("a", {}), "b": v.get("b", {})},
            {"type": "why",    "text": card.get("importance", "")},
            {"type": "verdict","text": v.get("verdict", "")},
        ]
    elif t == "data":
        slides = [
            {"type": "what",  "points": card.get("summary", []),
             "stats": card.get("stats") or []},
            {"type": "why",   "text": card.get("importance", "")},
        ]
    elif t == "timeline":
        slides = [
            {"type": "timeline", "items": card.get("timeline") or [],
             "points": card.get("summary", [])},
            {"type": "why",   "text": card.get("importance", "")},
        ]
    else:
        slides = [
            {"type": "what", "points": card.get("summary", [])},
            {"type": "why",  "text": card.get("importance", "")},
        ]

    slides.append({
        "type": "source",
        "url":      card.get("url", "#"),
        "score":    card.get("score", 0),
        "comments": card.get("comments", 0),
    })

    return {
        "title":    card.get("title_ko", ""),
        "subtitle": card.get("subtitle_ko") or "",
        "category": cat,
        "emoji":    CAT_EMOJI.get(cat, "📰"),
        "slides":   slides,
    }


CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --acc:#7C3AED; --acc-mid:#6D28D9; --acc-lt:#EDE9FE; --acc-xlt:#F5F3FF;
  --t1:#111827; --t2:#374151; --t3:#6B7280; --t4:#9CA3AF;
  --bg:#F0EEFF; --card:#fff; --border:#E5E7EB;
}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;
  background:var(--bg); color:var(--t1); min-height:100vh;
  padding-bottom:60px; overflow-x:hidden;
}

/* ── 페이지 헤더 ── */
.ph{text-align:center;padding:40px 20px 24px;}
.ph-label{
  display:inline-block;font-size:11px;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;color:var(--acc);background:var(--acc-lt);
  padding:4px 12px;border-radius:20px;margin-bottom:12px;
}
.ph-date{font-size:32px;font-weight:900;letter-spacing:-.02em;}
.ph-sub{font-size:14px;color:var(--t3);margin-top:6px;}

/* ── 오버뷰 그리드 ── */
.ov-grid{
  display:grid;grid-template-columns:repeat(2,1fr);
  gap:14px;max-width:520px;margin:0 auto;padding:0 16px;
}
/* 5번째 카드 중앙 정렬 */
.ov-card:nth-child(5){grid-column:1/-1;max-width:240px;margin:0 auto;width:100%;}

.ov-card{
  border-radius:20px;
  background:linear-gradient(145deg,#1E1B4B 0%,#5B21B6 100%);
  color:#fff;cursor:pointer;
  display:flex;flex-direction:column;
  padding:20px 18px 18px;
  aspect-ratio:3/4;
  position:relative;overflow:hidden;
  transition:transform .18s,box-shadow .18s;
  -webkit-tap-highlight-color:transparent;
}
.ov-card::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.08) 0%,transparent 60%);
}
.ov-card:hover{transform:scale(1.03);box-shadow:0 12px 40px rgba(109,40,217,.35);}
.ov-num{font-size:11px;font-weight:700;opacity:.45;letter-spacing:.05em;}
.ov-emoji{font-size:36px;margin:auto 0 12px;}
.ov-title{font-size:17px;font-weight:900;line-height:1.25;word-break:keep-all;}
.ov-cat{font-size:10px;font-weight:700;opacity:.5;text-transform:uppercase;
        letter-spacing:.08em;margin-top:6px;}
.ov-hint{
  margin-top:14px;font-size:11px;opacity:.45;font-weight:600;
  display:flex;align-items:center;gap:4px;
}

/* ── 디테일 패널 ── */
.dp{
  position:fixed;inset:0;z-index:200;
  display:flex;flex-direction:column;
  background:#fff;
  transform:translateY(100%);
  transition:transform .32s cubic-bezier(.4,0,.2,1);
}
.dp.open{transform:translateY(0);}

/* 프로그레스 바 */
.dp-bars{
  display:flex;gap:5px;padding:14px 16px 8px;flex-shrink:0;
}
.dp-bar{
  flex:1;height:3px;border-radius:2px;background:var(--border);
  transition:background .2s;
}
.dp-bar.done,.dp-bar.active{background:var(--acc);}

/* 헤더 */
.dp-head{
  display:flex;align-items:center;justify-content:space-between;
  padding:4px 16px 10px;flex-shrink:0;
}
.dp-news-title{
  font-size:13px;font-weight:700;color:var(--t3);
  flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.dp-close{
  background:var(--border);border:none;cursor:pointer;
  color:var(--t2);width:32px;height:32px;border-radius:50%;
  font-size:16px;display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin-left:8px;
}

/* 슬라이드 영역 */
.dp-slides{flex:1;overflow:hidden;position:relative;}
.dp-track{
  display:flex;height:100%;
  transition:transform .3s cubic-bezier(.4,0,.2,1);
  will-change:transform;
}

/* 네비 */
.dp-nav{
  display:flex;justify-content:space-between;align-items:center;
  padding:10px 20px 16px;flex-shrink:0;
}
.dp-nav-btn{
  background:var(--acc-xlt);border:none;
  width:44px;height:44px;border-radius:50%;
  font-size:20px;cursor:pointer;color:var(--acc);
  display:flex;align-items:center;justify-content:center;
  transition:background .15s;
}
.dp-nav-btn:hover{background:var(--acc-lt);}
.dp-nav-btn:disabled{opacity:.25;pointer-events:none;}
.dp-counter{font-size:13px;font-weight:700;color:var(--t4);}

/* ── 슬라이드 공통 ── */
.sl{
  flex-shrink:0;width:100%;height:100%;
  display:flex;flex-direction:column;justify-content:center;
  padding:36px 32px;overflow-y:auto;
}
.sl-label{
  font-size:12px;font-weight:800;color:var(--acc);
  letter-spacing:.1em;text-transform:uppercase;margin-bottom:24px;
}

/* Hook */
.sl-hook{
  background:linear-gradient(145deg,#1E1B4B 0%,#5B21B6 100%);
  color:#fff;justify-content:flex-end;padding-bottom:52px;
}
.sl-hook-emoji{font-size:56px;margin-bottom:16px;display:block;line-height:1;}
.sl-hook-cat{
  font-size:11px;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;opacity:.55;margin-bottom:10px;
}
.sl-hook-title{font-size:30px;font-weight:900;line-height:1.2;word-break:keep-all;}
.sl-hook-sub{
  font-size:16px;opacity:.65;margin-top:14px;
  line-height:1.55;font-style:italic;word-break:keep-all;
}

/* What */
.sl-what{background:#fff;}
.sl-bullets{list-style:none;display:flex;flex-direction:column;gap:18px;}
.sl-bullets li{
  font-size:19px;font-weight:700;color:var(--t1);
  line-height:1.4;padding-left:22px;position:relative;word-break:keep-all;
}
.sl-bullets li::before{
  content:'▸';position:absolute;left:0;
  color:var(--acc);font-size:14px;top:4px;
}

/* Why */
.sl-why{background:var(--acc-xlt);}
.sl-why-text{
  font-size:20px;font-weight:700;color:var(--t1);
  line-height:1.65;word-break:keep-all;
}

/* Versus */
.sl-versus{background:#fff;}
.vs-wrap{display:flex;gap:10px;align-items:flex-start;margin-top:4px;}
.vs-col{flex:1;}
.vs-name{
  font-size:14px;font-weight:900;color:var(--acc);
  text-align:center;margin-bottom:10px;
}
.vs-item{font-size:13px;color:var(--t2);margin-bottom:6px;line-height:1.4;}
.vs-spec{
  font-size:11px;font-weight:700;color:var(--acc);
  text-align:center;margin-top:8px;
}
.vs-sep{
  font-size:13px;font-weight:900;color:var(--acc);
  flex-shrink:0;padding-top:18px;
}

/* Verdict */
.sl-verdict{background:linear-gradient(145deg,var(--acc),var(--acc-mid));color:#fff;}
.sl-verdict .sl-label{color:rgba(255,255,255,.6);}
.sl-verdict-text{font-size:22px;font-weight:900;line-height:1.4;word-break:keep-all;}

/* Timeline */
.sl-tl{background:#fff;}
.tl-list{display:flex;flex-direction:column;gap:0;margin-top:8px;}
.tl-row{display:grid;grid-template-columns:52px 1px 1fr;gap:0 12px;}
.tl-date{
  font-size:11px;font-weight:700;color:var(--acc);
  text-align:right;padding:2px 0 16px;line-height:1.2;
}
.tl-line-w{display:flex;flex-direction:column;align-items:center;}
.tl-dot{
  width:10px;height:10px;border-radius:50%;
  background:var(--acc);flex-shrink:0;margin-top:2px;
}
.tl-line{flex:1;width:2px;background:var(--acc-lt);min-height:12px;}
.tl-row:last-child .tl-line{display:none;}
.tl-ev{font-size:14px;color:var(--t2);line-height:1.5;padding-bottom:16px;}
.tl-ev.cur{font-weight:700;color:var(--t1);}

/* Stats (data type) */
.stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:8px;}
.stat-box{
  background:var(--acc-xlt);border-radius:12px;
  padding:14px 8px;text-align:center;
}
.stat-val{font-size:22px;font-weight:900;color:var(--acc);line-height:1;}
.stat-unit{font-size:11px;color:var(--acc);font-weight:600;}
.stat-lbl{font-size:11px;color:var(--t3);margin-top:5px;line-height:1.3;}

/* Source */
.sl-source{background:#fff;align-items:center;text-align:center;gap:20px;}
.sl-source .sl-label{margin-bottom:8px;}
.src-link{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--acc);color:#fff;text-decoration:none;
  font-size:17px;font-weight:800;
  padding:16px 36px;border-radius:16px;
  transition:background .15s;
}
.src-link:hover{background:var(--acc-mid);}
.src-stats{font-size:16px;color:var(--t4);font-weight:600;}

/* ── 키워드 섹션 ── */
.kw-section{max-width:520px;margin:32px auto 0;padding:0 16px;}
.kw-head{display:flex;align-items:center;gap:10px;margin-bottom:14px;}
.kw-title{font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--acc);text-transform:uppercase;}
.kw-line{flex:1;height:1px;background:var(--acc-lt);}
.kw-list{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;}
@media(max-width:400px){.kw-list{grid-template-columns:1fr;}}
.kw-item{
  background:var(--card);border-radius:14px;padding:14px 16px;
  box-shadow:0 2px 16px rgba(109,40,217,.08);
  display:flex;flex-direction:column;gap:5px;
}
.kw-term{font-size:17px;font-weight:900;color:var(--acc);}
.kw-full{font-size:11px;color:var(--t4);}
.kw-desc{font-size:13px;color:var(--t2);line-height:1.6;word-break:keep-all;}

/* ── 내비게이션 ── */
.nav-bar{
  max-width:520px;margin:28px auto 0;padding:0 16px;
  display:flex;justify-content:space-between;
}
.nav-btn{
  font-size:13px;font-weight:700;color:var(--acc);
  text-decoration:none;background:var(--card);
  border-radius:10px;padding:9px 18px;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
}
.nav-btn.dis{color:var(--t4);pointer-events:none;box-shadow:none;}
"""

JS = """
const NEWS = __NEWS__;
const KWS  = __KWS__;

let cur = null, slide = 0;
let tx = 0;

function openDetail(i) {
  cur = i; slide = 0;
  const n = NEWS[i];
  const total = n.slides.length + 1;

  // bars
  const bars = document.getElementById('dp-bars');
  bars.innerHTML = Array.from({length: total}, (_,j) =>
    `<div class="dp-bar${j===0?' active':''}"></div>`).join('');

  // title
  document.getElementById('dp-title').textContent = n.title;

  // build slides
  const track = document.getElementById('dp-track');
  track.style.transition = 'none';
  track.style.transform = 'translateX(0)';

  let html = slideHook(n);
  n.slides.forEach(s => { html += buildSlide(s); });
  track.innerHTML = html;

  updateNav(total);
  document.getElementById('dp').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeDetail() {
  document.getElementById('dp').classList.remove('open');
  document.body.style.overflow = '';
}

function go(dir) {
  if (!NEWS[cur]) return;
  const total = NEWS[cur].slides.length + 1;
  slide = Math.max(0, Math.min(total - 1, slide + dir));
  const track = document.getElementById('dp-track');
  track.style.transition = 'transform .28s cubic-bezier(.4,0,.2,1)';
  track.style.transform = `translateX(-${slide * 100}%)`;
  const bars = document.querySelectorAll('.dp-bar');
  bars.forEach((b,i) => {
    b.classList.toggle('active', i === slide);
    b.classList.toggle('done', i < slide);
  });
  updateNav(total);
  document.getElementById('dp-counter').textContent = `${slide+1} / ${total}`;
}

function updateNav(total) {
  document.getElementById('dp-prev').disabled = slide === 0;
  document.getElementById('dp-next').disabled = slide === total - 1;
  document.getElementById('dp-counter').textContent = `${slide+1} / ${total}`;
}

/* ── Slide builders ── */
function slideHook(n) {
  return `<div class="sl sl-hook">
    <span class="sl-hook-emoji">${n.emoji}</span>
    <p class="sl-hook-cat">${n.category}</p>
    <h1 class="sl-hook-title">${n.title}</h1>
    ${n.subtitle ? `<p class="sl-hook-sub">"${n.subtitle}"</p>` : ''}
  </div>`;
}

function buildSlide(s) {
  switch(s.type) {
    case 'what': {
      const bullets = (s.points||[]).map(p => `<li>${p}</li>`).join('');
      const statsHtml = buildStats(s.stats);
      return `<div class="sl sl-what">
        <p class="sl-label">무슨 일?</p>
        ${statsHtml}
        <ul class="sl-bullets">${bullets}</ul>
      </div>`;
    }
    case 'why':
      return `<div class="sl sl-why">
        <p class="sl-label">왜 중요해?</p>
        <p class="sl-why-text">${s.text}</p>
      </div>`;
    case 'versus': {
      const a = s.a||{}, b = s.b||{};
      const col = side => `<div class="vs-col">
        <p class="vs-name">${side.name||''}</p>
        ${(side.pros||[]).map(p=>`<p class="vs-item">✅ ${p}</p>`).join('')}
        ${(side.cons||[]).map(c=>`<p class="vs-item">❌ ${c}</p>`).join('')}
        ${side.spec?`<p class="vs-spec">${side.spec}</p>`:''}
      </div>`;
      return `<div class="sl sl-versus">
        <p class="sl-label">비교</p>
        <div class="vs-wrap">${col(a)}<div class="vs-sep">VS</div>${col(b)}</div>
      </div>`;
    }
    case 'verdict':
      return `<div class="sl sl-verdict">
        <p class="sl-label">🏆 결론</p>
        <p class="sl-verdict-text">${s.text}</p>
      </div>`;
    case 'timeline': {
      const items = (s.items||[]);
      const rows = items.map((t,i) =>
        `<div class="tl-row">
          <p class="tl-date">${t.date||''}</p>
          <div class="tl-line-w"><div class="tl-dot"></div><div class="tl-line"></div></div>
          <p class="tl-ev${i===items.length-1?' cur':''}">${t.event||''}</p>
        </div>`).join('');
      return `<div class="sl sl-tl">
        <p class="sl-label">타임라인</p>
        <div class="tl-list">${rows}</div>
      </div>`;
    }
    case 'source':
      return `<div class="sl sl-source">
        <p class="sl-label">원문 보기</p>
        <a class="src-link" href="${s.url}" target="_blank">자세히 읽기 →</a>
        <p class="src-stats">⬆ ${s.score} &nbsp;&nbsp; 💬 ${s.comments}</p>
      </div>`;
    default: return '';
  }
}

function buildStats(stats) {
  if (!stats || !stats.length) return '';
  const boxes = stats.slice(0,3).map(s =>
    `<div class="stat-box">
      <p class="stat-val">${s.value}<span class="stat-unit">${s.unit||''}</span></p>
      <p class="stat-lbl">${s.label}</p>
    </div>`).join('');
  return `<div class="stat-grid">${boxes}</div>`;
}

/* ── Touch / Keyboard ── */
document.addEventListener('DOMContentLoaded', () => {
  const dp = document.getElementById('dp');
  let tsx = 0;
  dp.addEventListener('touchstart', e => { tsx = e.touches[0].clientX; }, {passive:true});
  dp.addEventListener('touchend',   e => {
    const diff = tsx - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 48) diff > 0 ? go(1) : go(-1);
  }, {passive:true});

  document.addEventListener('keydown', e => {
    if (!dp.classList.contains('open')) return;
    if (e.key==='ArrowRight') go(1);
    if (e.key==='ArrowLeft')  go(-1);
    if (e.key==='Escape')     closeDetail();
  });
});
"""


def generate_page(cards, date_str, keywords=None, prev_date=None, next_date=None):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    date_display = dt.strftime("%Y년 %m월 %d일")
    dow = ["월","화","수","목","금","토","일"][dt.weekday()]
    total = len(cards)

    # Overview cards HTML
    ov_html = ""
    for i, card in enumerate(cards, 1):
        emoji = CAT_EMOJI.get(card.get("category","기타"), "📰")
        title = card.get("title_ko", "")
        cat   = card.get("category", "기타")
        ov_html += f"""<div class="ov-card" onclick="openDetail({i-1})">
      <p class="ov-num">{i:02d}</p>
      <span class="ov-emoji">{emoji}</span>
      <h2 class="ov-title">{title}</h2>
      <p class="ov-cat">{cat}</p>
      <p class="ov-hint">탭해서 보기 ›</p>
    </div>"""

    # Keywords section
    kw_html = ""
    if keywords:
        items = ""
        for kw in keywords:
            full = f'<p class="kw-full">{kw["full"]}</p>' if kw.get("full") else ""
            items += f"""<div class="kw-item">
          <p class="kw-term">{kw['term']}</p>
          {full}
          <p class="kw-desc">{kw['desc']}</p>
        </div>"""
        kw_html = f"""<section class="kw-section">
    <div class="kw-head">
      <span class="kw-title">오늘의 키워드</span>
      <div class="kw-line"></div>
    </div>
    <div class="kw-list">{items}</div>
  </section>"""

    prev_link = f'<a class="nav-btn" href="{prev_date}.html">← {prev_date}</a>' if prev_date else '<span class="nav-btn dis">← 이전</span>'
    next_link = f'<a class="nav-btn" href="{next_date}.html">{next_date} →</a>' if next_date else '<span class="nav-btn dis">다음 →</span>'

    news_json = json.dumps([card_to_js(c) for c in cards], ensure_ascii=False)
    kws_json  = json.dumps(keywords or [], ensure_ascii=False)
    js = JS.replace("__NEWS__", news_json).replace("__KWS__", kws_json)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
  <title>IT 카드뉴스 — {date_display}</title>
  <style>{CSS}</style>
</head>
<body>

<header class="ph">
  <p class="ph-label">IT 카드뉴스</p>
  <h1 class="ph-date">{date_display} ({dow})</h1>
  <p class="ph-sub">오늘의 핵심 뉴스 {total}선 · 탭해서 보기</p>
</header>

<div class="ov-grid">{ov_html}</div>

{kw_html}

<nav class="nav-bar">{prev_link}{next_link}</nav>

<!-- ── 디테일 패널 ── -->
<div class="dp" id="dp">
  <div class="dp-bars" id="dp-bars"></div>
  <div class="dp-head">
    <p class="dp-news-title" id="dp-title"></p>
    <button class="dp-close" onclick="closeDetail()">✕</button>
  </div>
  <div class="dp-slides">
    <div class="dp-track" id="dp-track"></div>
  </div>
  <div class="dp-nav">
    <button class="dp-nav-btn" id="dp-prev" onclick="go(-1)" disabled>←</button>
    <span class="dp-counter" id="dp-counter"></span>
    <button class="dp-nav-btn" id="dp-next" onclick="go(1)">→</button>
  </div>
</div>

<script>{js}</script>
</body>
</html>"""


def generate_index(dates):
    items = ""
    for d in sorted(dates, reverse=True):
        dt = datetime.strptime(d, "%Y-%m-%d")
        label = dt.strftime("%Y.%m.%d")
        dow = ["월","화","수","목","금","토","일"][dt.weekday()]
        items += f'<a class="idx-item" href="{d}.html"><span class="idx-date">{label}</span><span class="idx-dow">{dow}요일</span></a>\n'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>IT 카드뉴스 아카이브</title>
  <style>
    {CSS}
    .idx-wrap{{max-width:480px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:10px;}}
    .idx-item{{display:flex;justify-content:space-between;align-items:center;
      background:#fff;border-radius:14px;padding:16px 20px;text-decoration:none;
      box-shadow:0 2px 16px rgba(109,40,217,.08);transition:background .15s;}}
    .idx-item:hover{{background:var(--acc-lt);}}
    .idx-date{{font-size:18px;font-weight:800;color:var(--t1);}}
    .idx-dow{{font-size:13px;color:var(--acc);font-weight:600;}}
  </style>
</head>
<body>
  <header class="ph">
    <p class="ph-label">IT 카드뉴스</p>
    <h1 class="ph-date">아카이브</h1>
    <p class="ph-sub">지난 뉴스 모아보기</p>
  </header>
  <div class="idx-wrap">{items}</div>
</body>
</html>"""
