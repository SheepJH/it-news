import json
from datetime import datetime

CAT_EMOJI = {
    "AI/ML": "🤖", "보안": "🔐", "개발": "💻",
    "비즈니스": "📈", "기타": "📰",
}

# ── 슬라이드 데이터 구성 ────────────────────────────────────────────────────
# 슬라이드 순서 원칙:
#   HOOK(dark) → 콘텐츠들(밝↔어두 교차) → WHY(accent) → TAKEAWAY(dark) → SOURCE(light)

def card_to_js(card):
    cat   = card.get("category", "기타")
    t     = card.get("type", "standard")
    pts   = card.get("points") or card.get("summary") or []
    imp   = card.get("importance", "")
    tkwy  = card.get("takeaway", "")
    src   = {"type": "source", "url": card.get("url","#"),
             "score": card.get("score",0), "comments": card.get("comments",0)}

    if t == "versus":
        v = card.get("versus") or {}
        a, b = v.get("a",{}), v.get("b",{})
        slides = [
            {"type": "profile", "dark": False, "name": a.get("name",""),
             "text": a.get("highlight",""), "spec": a.get("spec",""),
             "pros": a.get("pros",[]), "cons": a.get("cons",[])},
            {"type": "profile", "dark": True,  "name": b.get("name",""),
             "text": b.get("highlight",""), "spec": b.get("spec",""),
             "pros": b.get("pros",[]), "cons": b.get("cons",[])},
            {"type": "versus", "a": a, "b": b},
            {"type": "verdict", "text": v.get("verdict","")},
            {"type": "why",      "text": imp},
            {"type": "takeaway", "text": tkwy},
            src,
        ]

    elif t == "data":
        stats = card.get("stats") or []
        slides = []
        for i, st in enumerate(stats[:3]):
            slides.append({"type": "bignum", "dark": i % 2 == 1,
                           "value": st.get("value",""), "unit": st.get("unit",""),
                           "label": st.get("label","")})
        slides += [
            {"type": "why",      "text": imp},
            {"type": "takeaway", "text": tkwy},
            src,
        ]

    elif t == "timeline":
        tl = card.get("timeline") or []
        slides = [
            {"type": "timeline", "items": tl},
            {"type": "point",    "dark": True,  "n": 1, "text": pts[0]} if pts else None,
            {"type": "why",      "text": imp},
            {"type": "takeaway", "text": tkwy},
            src,
        ]
        slides = [s for s in slides if s]

    else:  # standard / explainer
        slides = []
        for i, p in enumerate(pts[:3]):
            slides.append({"type": "point", "dark": i % 2 == 1, "n": i+1, "text": p})
        slides += [
            {"type": "why",      "text": imp},
            {"type": "takeaway", "text": tkwy},
            src,
        ]

    return {
        "title":    card.get("title_ko",""),
        "subtitle": card.get("subtitle_ko") or "",
        "category": cat,
        "emoji":    CAT_EMOJI.get(cat, "📰"),
        "slides":   slides,
    }


# ── CSS ─────────────────────────────────────────────────────────────────────
CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --lt:#FAFAF8; --dk:#0F0F1A; --acc:#7C3AED; --acc-mid:#5B21B6;
  --acc-glow:#A78BFA; --acc-pale:#EDE9FE; --acc-xlt:#F5F3FF;
  --t1:#111; --t2:#444; --t3:#888; --t4:#bbb; --border:#E5E7EB;
}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR','Apple SD Gothic Neo',sans-serif;
  background:#F0EEFF;color:var(--t1);min-height:100vh;
  padding-bottom:60px;overflow-x:hidden;
}

/* ── 페이지 헤더 ── */
.ph{text-align:center;padding:44px 20px 24px;}
.ph-chip{
  display:inline-block;font-size:11px;font-weight:800;letter-spacing:.12em;
  text-transform:uppercase;color:var(--acc);background:var(--acc-pale);
  padding:5px 14px;border-radius:20px;margin-bottom:14px;
}
.ph-date{font-size:34px;font-weight:900;letter-spacing:-.025em;color:var(--dk);}
.ph-sub{font-size:14px;color:var(--t3);margin-top:8px;}

/* ── 오버뷰 그리드 ── */
.ov-grid{
  display:grid;grid-template-columns:repeat(2,1fr);
  gap:12px;max-width:500px;margin:0 auto;padding:0 16px;
}
.ov-card:nth-child(5){grid-column:1/-1;max-width:230px;margin:0 auto;width:100%;}
.ov-card{
  border-radius:22px;background:var(--dk);color:#fff;cursor:pointer;
  display:flex;flex-direction:column;padding:22px 18px 20px;
  aspect-ratio:3/4;position:relative;overflow:hidden;
  -webkit-tap-highlight-color:transparent;transition:transform .18s;
}
.ov-card::before{
  content:'';position:absolute;top:-28px;right:-28px;
  width:110px;height:110px;border-radius:50%;
  background:var(--acc);opacity:.15;
}
.ov-card:hover{transform:scale(1.03);}
.ov-num{font-size:11px;font-weight:800;color:var(--acc-glow);opacity:.7;letter-spacing:.08em;}
.ov-emoji{font-size:40px;margin:auto 0 12px;display:block;line-height:1;}
.ov-title{font-size:16px;font-weight:900;line-height:1.25;word-break:keep-all;letter-spacing:-.01em;}
.ov-cat{font-size:10px;font-weight:700;color:var(--acc-glow);opacity:.55;text-transform:uppercase;letter-spacing:.08em;margin-top:6px;}
.ov-tap{margin-top:14px;font-size:11px;color:rgba(255,255,255,.28);font-weight:600;}

/* ── 디테일 패널 ── */
.dp{
  position:fixed;inset:0;z-index:200;display:flex;flex-direction:column;
  background:var(--dk);
  transform:translateY(105%);transition:transform .35s cubic-bezier(.4,0,.15,1);
}
.dp.open{transform:translateY(0);}
.dp-bars{
  display:flex;gap:4px;
  padding:max(env(safe-area-inset-top),14px) 16px 10px;
  flex-shrink:0;
}
.dp-bar{flex:1;height:3px;border-radius:2px;background:rgba(255,255,255,.12);transition:background .2s;}
.dp-bar.done,.dp-bar.active{background:var(--acc-glow);}
.dp-head{display:flex;align-items:center;padding:4px 16px 10px;flex-shrink:0;}
.dp-news-title{
  font-size:13px;font-weight:700;color:rgba(255,255,255,.35);
  flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.dp-close{
  background:rgba(255,255,255,.08);border:none;cursor:pointer;
  color:rgba(255,255,255,.6);width:32px;height:32px;border-radius:50%;
  font-size:15px;display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin-left:10px;
}
.dp-slides{flex:1;overflow:hidden;position:relative;}
.dp-track{display:flex;height:100%;transition:transform .28s cubic-bezier(.4,0,.2,1);will-change:transform;}
.dp-nav{
  display:flex;justify-content:space-between;align-items:center;
  padding:10px 20px max(env(safe-area-inset-bottom),14px);
  flex-shrink:0;background:var(--dk);
}
.dp-btn{
  background:rgba(255,255,255,.08);border:none;
  width:44px;height:44px;border-radius:50%;
  font-size:20px;cursor:pointer;color:rgba(255,255,255,.7);
  display:flex;align-items:center;justify-content:center;transition:background .15s;
}
.dp-btn:hover{background:rgba(255,255,255,.18);}
.dp-btn:disabled{opacity:.18;pointer-events:none;}
.dp-cnt{font-size:13px;font-weight:700;color:rgba(255,255,255,.25);}

/* ── 슬라이드 공통 ── */
.sl{flex-shrink:0;width:100%;height:100%;display:flex;flex-direction:column;padding:44px 36px;overflow-y:auto;position:relative;}
.sl-lbl{
  font-size:10px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;
  margin-bottom:16px;display:flex;align-items:center;gap:10px;
}
.sl-bar{height:3px;width:28px;border-radius:2px;flex-shrink:0;}

/* ══ 1. HOOK (dark navy) ══ */
.sl-hook{background:var(--dk);color:#fff;justify-content:flex-end;padding-bottom:52px;}
.sl-hook .sl-lbl{color:var(--acc-glow);}
.sl-hook .sl-bar{background:var(--acc);}
.hook-emoji{font-size:68px;margin-bottom:20px;display:block;line-height:1;}
.hook-title{font-size:40px;font-weight:900;line-height:1.15;word-break:keep-all;letter-spacing:-.025em;}
.hook-sub{font-size:16px;color:rgba(255,255,255,.42);margin-top:14px;line-height:1.65;font-style:italic;word-break:keep-all;}

/* ══ 2. POINT — light ══ */
.sl-pt-lt{background:var(--lt);color:var(--t1);}
.sl-pt-lt .sl-lbl{color:var(--acc);}
.sl-pt-lt .sl-bar{background:var(--acc);}
.pt-num-bg{
  position:absolute;right:20px;bottom:24px;
  font-size:140px;font-weight:900;color:rgba(0,0,0,.04);
  line-height:1;letter-spacing:-.04em;user-select:none;pointer-events:none;
}
.pt-text{font-size:25px;font-weight:700;line-height:1.65;word-break:keep-all;letter-spacing:-.01em;}

/* ══ 3. POINT — dark ══ */
.sl-pt-dk{background:var(--dk);color:#fff;}
.sl-pt-dk .sl-lbl{color:var(--acc-glow);}
.sl-pt-dk .sl-bar{background:var(--acc-glow);}
.sl-pt-dk .pt-num-bg{color:rgba(255,255,255,.04);}
.sl-pt-dk .pt-text{color:rgba(255,255,255,.88);}

/* ══ 4. PROFILE A (light) ══ */
.sl-prof-lt{background:var(--lt);}
.sl-prof-lt .sl-lbl{color:var(--acc);}
.sl-prof-lt .sl-bar{background:var(--acc);}
.prof-name{font-size:38px;font-weight:900;letter-spacing:-.02em;margin-bottom:16px;word-break:keep-all;}
.sl-prof-lt .prof-name{color:var(--dk);}
.prof-text{font-size:20px;font-weight:600;line-height:1.65;word-break:keep-all;color:var(--t2);}
.prof-spec{
  margin-top:20px;display:inline-block;
  font-size:13px;font-weight:800;color:var(--acc);
  background:var(--acc-pale);padding:6px 14px;border-radius:20px;
}

/* ══ 5. PROFILE B (dark) ══ */
.sl-prof-dk{background:var(--dk);}
.sl-prof-dk .sl-lbl{color:var(--acc-glow);}
.sl-prof-dk .sl-bar{background:var(--acc-glow);}
.sl-prof-dk .prof-name{color:var(--acc-glow);}
.sl-prof-dk .prof-text{color:rgba(255,255,255,.75);}
.sl-prof-dk .prof-spec{color:var(--acc-glow);background:rgba(167,139,250,.15);}

/* ══ 6. VERSUS HEAD-TO-HEAD ══ */
.sl-versus{background:var(--lt);}
.sl-versus .sl-lbl{color:var(--acc);}
.sl-versus .sl-bar{background:var(--acc);}
.vs-cols{display:flex;gap:10px;margin-top:10px;align-items:stretch;}
.vs-col-a{flex:1;background:#F3F4F6;border-radius:18px;padding:18px 14px;}
.vs-col-b{flex:1;background:var(--dk);border-radius:18px;padding:18px 14px;}
.vs-col-name{font-size:16px;font-weight:900;margin-bottom:10px;}
.vs-col-b .vs-col-name{color:var(--acc-glow);}
.vs-col-it{font-size:13px;line-height:1.45;margin-bottom:5px;color:var(--t2);}
.vs-col-b .vs-col-it{color:rgba(255,255,255,.72);}
.vs-col-spec{font-size:12px;font-weight:800;margin-top:10px;color:var(--acc);}
.vs-col-b .vs-col-spec{color:var(--acc-glow);}
.vs-mid{font-size:13px;font-weight:900;color:var(--acc);align-self:center;flex-shrink:0;}

/* ══ 7. VERDICT (dark) ══ */
.sl-verdict{background:var(--dk);color:#fff;justify-content:center;}
.sl-verdict .sl-lbl{color:var(--acc-glow);}
.sl-verdict .sl-bar{background:var(--acc-glow);}
.verdict-icon{font-size:52px;margin-bottom:18px;display:block;}
.verdict-text{font-size:26px;font-weight:900;line-height:1.4;word-break:keep-all;letter-spacing:-.015em;}

/* ══ 8. BIG NUMBER (light) ══ */
.sl-num-lt{background:var(--lt);}
.sl-num-lt .sl-lbl{color:var(--acc);}
.sl-num-lt .sl-bar{background:var(--acc);}
.bignum{font-size:100px;font-weight:900;letter-spacing:-.04em;line-height:1;color:var(--dk);}
.bignum-unit{font-size:36px;font-weight:800;color:var(--acc);}
.bignum-label{font-size:17px;color:var(--t3);margin-top:12px;font-weight:600;line-height:1.4;}

/* ══ 9. BIG NUMBER (dark) ══ */
.sl-num-dk{background:var(--dk);}
.sl-num-dk .sl-lbl{color:var(--acc-glow);}
.sl-num-dk .sl-bar{background:var(--acc-glow);}
.sl-num-dk .bignum{color:#fff;}
.sl-num-dk .bignum-unit{color:var(--acc-glow);}
.sl-num-dk .bignum-label{color:rgba(255,255,255,.38);}

/* ══ 10. TIMELINE ══ */
.sl-tl{background:var(--lt);}
.sl-tl .sl-lbl{color:var(--acc);}
.sl-tl .sl-bar{background:var(--acc);}
.tl-rows{display:flex;flex-direction:column;margin-top:10px;}
.tl-row{display:grid;grid-template-columns:52px 14px 1fr;gap:0 14px;}
.tl-date{font-size:11px;font-weight:800;color:var(--acc);text-align:right;padding:1px 0 18px;line-height:1.3;}
.tl-dot-w{display:flex;flex-direction:column;align-items:center;}
.tl-dot{width:12px;height:12px;border-radius:50%;background:var(--acc);flex-shrink:0;margin-top:1px;}
.tl-conn{flex:1;width:2px;background:var(--acc-pale);min-height:10px;}
.tl-row:last-child .tl-conn{display:none;}
.tl-ev{font-size:15px;font-weight:600;color:var(--t1);line-height:1.5;padding-bottom:18px;word-break:keep-all;}
.tl-ev.cur{font-weight:900;color:var(--acc-mid);}

/* ══ 11. WHY (accent gradient) ══ */
.sl-why{
  background:linear-gradient(155deg,#2E1065 0%,var(--acc-mid) 100%);
  color:#fff;justify-content:center;position:relative;overflow:hidden;
}
.sl-why::after{
  content:'"';position:absolute;right:-15px;bottom:-50px;
  font-size:300px;font-weight:900;font-family:Georgia,serif;
  color:rgba(255,255,255,.05);line-height:1;user-select:none;pointer-events:none;
}
.sl-why .sl-lbl{color:var(--acc-glow);}
.sl-why .sl-bar{background:var(--acc-glow);}
.why-text{font-size:22px;font-weight:800;line-height:1.65;word-break:keep-all;position:relative;z-index:1;}

/* ══ 12. TAKEAWAY (dark + yellow accent) ══ */
.sl-tkwy{background:var(--dk);color:#fff;justify-content:center;}
.sl-tkwy .sl-lbl{color:#FCD34D;}
.sl-tkwy .sl-bar{background:#FCD34D;}
.tkwy-icon{font-size:52px;margin-bottom:18px;display:block;}
.tkwy-text{font-size:23px;font-weight:800;line-height:1.6;word-break:keep-all;}

/* ══ 13. SOURCE (light) ══ */
.sl-src{background:var(--lt);align-items:center;justify-content:center;text-align:center;}
.sl-src .sl-lbl{color:var(--acc);justify-content:center;}
.sl-src .sl-bar{display:none;}
.src-emoji{font-size:52px;margin-bottom:24px;display:block;}
.src-btn{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--dk);color:#fff;text-decoration:none;
  font-size:17px;font-weight:800;padding:18px 40px;border-radius:100px;
  transition:background .15s;
}
.src-btn:hover{background:var(--acc-mid);}
.src-stats{font-size:15px;color:var(--t4);font-weight:600;margin-top:20px;}

/* ── 키워드 섹션 ── */
.kw-wrap{max-width:500px;margin:32px auto 0;padding:0 16px;}
.kw-head{display:flex;align-items:center;gap:10px;margin-bottom:14px;}
.kw-head-lbl{font-size:11px;font-weight:800;letter-spacing:.12em;color:var(--acc);text-transform:uppercase;white-space:nowrap;}
.kw-head-line{flex:1;height:1px;background:var(--acc-pale);}
.kw-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;}
@media(max-width:380px){.kw-grid{grid-template-columns:1fr;}}
.kw-card{
  background:#fff;border-radius:14px;padding:14px 16px;
  box-shadow:0 2px 14px rgba(109,40,217,.08);
  display:flex;flex-direction:column;gap:5px;
}
.kw-term{font-size:17px;font-weight:900;color:var(--acc);}
.kw-full{font-size:11px;color:var(--t4);}
.kw-desc{font-size:13px;color:var(--t2);line-height:1.6;word-break:keep-all;}

/* ── 내비 ── */
.nav-bar{max-width:500px;margin:28px auto 0;padding:0 16px;display:flex;justify-content:space-between;}
.nav-a{font-size:13px;font-weight:700;color:var(--acc);text-decoration:none;background:#fff;border-radius:10px;padding:9px 18px;box-shadow:0 2px 8px rgba(0,0,0,.06);}
.nav-a.dis{color:var(--t4);pointer-events:none;box-shadow:none;}
"""


# ── JavaScript ──────────────────────────────────────────────────────────────
JS = r"""
const NEWS=__NEWS__;
let cur=null,slide=0,tsx=0;

function openDetail(i){
  cur=i;slide=0;
  const n=NEWS[i],total=n.slides.length+1;
  document.getElementById('dp-bars').innerHTML=
    Array.from({length:total},(_,j)=>`<div class="dp-bar${j===0?' active':''}"></div>`).join('');
  document.getElementById('dp-title').textContent=n.title;
  const track=document.getElementById('dp-track');
  track.style.transition='none';track.style.transform='translateX(0)';
  track.innerHTML=buildHook(n)+n.slides.map(buildSlide).join('');
  updateNav(total);
  document.getElementById('dp').classList.add('open');
  document.body.style.overflow='hidden';
}
function closeDetail(){
  document.getElementById('dp').classList.remove('open');
  document.body.style.overflow='';
}
function go(d){
  if(cur===null)return;
  const total=NEWS[cur].slides.length+1;
  slide=Math.max(0,Math.min(total-1,slide+d));
  const track=document.getElementById('dp-track');
  track.style.transition='transform .28s cubic-bezier(.4,0,.2,1)';
  track.style.transform=`translateX(-${slide*100}%)`;
  document.querySelectorAll('.dp-bar').forEach((b,i)=>{
    b.classList.toggle('active',i===slide);
    b.classList.toggle('done',i<slide);
  });
  updateNav(total);
}
function updateNav(total){
  document.getElementById('dp-prev').disabled=slide===0;
  document.getElementById('dp-next').disabled=slide===total-1;
  document.getElementById('dp-cnt').textContent=`${slide+1} / ${total}`;
}

/* ── 슬라이드 라벨 헬퍼 ── */
function lbl(text,cls=''){
  return `<div class="sl-lbl ${cls}">${text}<div class="sl-bar"></div></div>`;
}

/* ── HOOK ── */
function buildHook(n){
  return `<div class="sl sl-hook">
    <span class="hook-emoji">${n.emoji}</span>
    ${lbl(n.category)}
    <h1 class="hook-title">${n.title}</h1>
    ${n.subtitle?`<p class="hook-sub">"${n.subtitle}"</p>`:''}
  </div>`;
}

/* ── 슬라이드 빌더 ── */
function buildSlide(s){
  switch(s.type){

    /* POINT */
    case 'point': {
      const cls = s.dark ? 'sl-pt-dk' : 'sl-pt-lt';
      return `<div class="sl ${cls}">
        ${lbl(`POINT ${String(s.n).padStart(2,'0')}`)}
        <p class="pt-text">${s.text}</p>
        <span class="pt-num-bg">${s.n}</span>
      </div>`;}

    /* PROFILE (versus 단면) */
    case 'profile': {
      const cls = s.dark ? 'sl-prof-dk' : 'sl-prof-lt';
      const pros = (s.pros||[]).map(p=>`<p class="prof-text" style="margin-bottom:6px">✅ ${p}</p>`).join('');
      const cons = (s.cons||[]).map(c=>`<p class="prof-text" style="margin-bottom:6px">❌ ${c}</p>`).join('');
      return `<div class="sl ${cls}">
        ${lbl(s.dark ? 'SIDE B' : 'SIDE A')}
        <p class="prof-name">${s.name}</p>
        <p class="prof-text" style="margin-bottom:16px">${s.text}</p>
        ${pros}${cons}
        ${s.spec?`<span class="prof-spec">${s.spec}</span>`:''}
      </div>`;}

    /* VERSUS 대결 */
    case 'versus': {
      const a=s.a||{}, b=s.b||{};
      const col=(side,cls)=>`<div class="${cls}">
        <p class="vs-col-name">${side.name||''}</p>
        ${(side.pros||[]).map(p=>`<p class="vs-col-it">✅ ${p}</p>`).join('')}
        ${(side.cons||[]).map(c=>`<p class="vs-col-it">❌ ${c}</p>`).join('')}
        ${side.spec?`<p class="vs-col-spec">${side.spec}</p>`:''}
      </div>`;
      return `<div class="sl sl-versus">
        ${lbl('HEAD TO HEAD')}
        <div class="vs-cols">
          ${col(a,'vs-col-a')}
          <div class="vs-mid">VS</div>
          ${col(b,'vs-col-b')}
        </div>
      </div>`;}

    /* VERDICT */
    case 'verdict':
      return `<div class="sl sl-verdict">
        <span class="verdict-icon">🏆</span>
        ${lbl('결론')}
        <p class="verdict-text">${s.text}</p>
      </div>`;

    /* BIG NUMBER */
    case 'bignum': {
      const cls = s.dark ? 'sl-num-dk' : 'sl-num-lt';
      return `<div class="sl ${cls}">
        ${lbl('KEY NUMBER')}
        <p class="bignum">${s.value}<span class="bignum-unit">${s.unit||''}</span></p>
        <p class="bignum-label">${s.label}</p>
      </div>`;}

    /* TIMELINE */
    case 'timeline': {
      const rows=(s.items||[]).map((t,i,arr)=>`
        <div class="tl-row">
          <p class="tl-date">${t.date||''}</p>
          <div class="tl-dot-w"><div class="tl-dot"></div><div class="tl-conn"></div></div>
          <p class="tl-ev${i===arr.length-1?' cur':''}">${t.event||''}</p>
        </div>`).join('');
      return `<div class="sl sl-tl">
        ${lbl('타임라인')}
        <div class="tl-rows">${rows}</div>
      </div>`;}

    /* WHY */
    case 'why':
      return `<div class="sl sl-why">
        ${lbl('왜 중요해?')}
        <p class="why-text">${s.text}</p>
      </div>`;

    /* TAKEAWAY */
    case 'takeaway':
      return `<div class="sl sl-tkwy">
        <span class="tkwy-icon">💡</span>
        ${lbl('지금 바로 알아야 할 것')}
        <p class="tkwy-text">${s.text}</p>
      </div>`;

    /* SOURCE */
    case 'source':
      return `<div class="sl sl-src">
        ${lbl('원문 보기')}
        <span class="src-emoji">📖</span>
        <a class="src-btn" href="${s.url}" target="_blank">자세히 읽기 →</a>
        <p class="src-stats">⬆ ${s.score}&nbsp;&nbsp;💬 ${s.comments}</p>
      </div>`;

    default: return '';
  }
}

/* ── Touch / Keyboard ── */
document.addEventListener('DOMContentLoaded',()=>{
  const dp=document.getElementById('dp');
  dp.addEventListener('touchstart',e=>{tsx=e.touches[0].clientX;},{passive:true});
  dp.addEventListener('touchend',e=>{
    const d=tsx-e.changedTouches[0].clientX;
    if(Math.abs(d)>48) d>0?go(1):go(-1);
  },{passive:true});
  document.addEventListener('keydown',e=>{
    if(!dp.classList.contains('open'))return;
    if(e.key==='ArrowRight')go(1);
    if(e.key==='ArrowLeft') go(-1);
    if(e.key==='Escape')    closeDetail();
  });
});
"""


# ── 페이지 생성 ──────────────────────────────────────────────────────────────
def generate_page(cards, date_str, keywords=None, prev_date=None, next_date=None):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    date_display = dt.strftime("%Y년 %m월 %d일")
    dow = ["월","화","수","목","금","토","일"][dt.weekday()]
    total = len(cards)

    ov = ""
    for i, c in enumerate(cards, 1):
        emoji = CAT_EMOJI.get(c.get("category","기타"), "📰")
        ov += f"""<div class="ov-card" onclick="openDetail({i-1})">
      <p class="ov-num">{i:02d}</p>
      <span class="ov-emoji">{emoji}</span>
      <h2 class="ov-title">{c.get('title_ko','')}</h2>
      <p class="ov-cat">{c.get('category','기타')}</p>
      <p class="ov-tap">탭해서 보기 ›</p>
    </div>"""

    kw = ""
    if keywords:
        items = "".join(f"""<div class="kw-card">
          <p class="kw-term">{k['term']}</p>
          {f'<p class="kw-full">{k["full"]}</p>' if k.get('full') else ''}
          <p class="kw-desc">{k['desc']}</p>
        </div>""" for k in keywords)
        kw = f"""<section class="kw-wrap">
    <div class="kw-head">
      <span class="kw-head-lbl">오늘의 키워드</span>
      <div class="kw-head-line"></div>
    </div>
    <div class="kw-grid">{items}</div>
  </section>"""

    prev_a = f'<a class="nav-a" href="{prev_date}.html">← {prev_date}</a>' if prev_date else '<span class="nav-a dis">← 이전</span>'
    next_a = f'<a class="nav-a" href="{next_date}.html">{next_date} →</a>' if next_date else '<span class="nav-a dis">다음 →</span>'

    news_json = json.dumps([card_to_js(c) for c in cards], ensure_ascii=False)
    js = JS.replace("__NEWS__", news_json)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
  <title>IT 카드뉴스 — {date_display}</title>
  <style>{CSS}</style>
</head>
<body>

<header class="ph">
  <p class="ph-chip">IT 카드뉴스</p>
  <h1 class="ph-date">{date_display} ({dow})</h1>
  <p class="ph-sub">오늘의 핵심 뉴스 {total}선 · 탭해서 슬라이드로 보기</p>
</header>

<div class="ov-grid">{ov}</div>
{kw}
<nav class="nav-bar">{prev_a}{next_a}</nav>

<div class="dp" id="dp">
  <div class="dp-bars" id="dp-bars"></div>
  <div class="dp-head">
    <p class="dp-news-title" id="dp-title"></p>
    <button class="dp-close" onclick="closeDetail()">✕</button>
  </div>
  <div class="dp-slides"><div class="dp-track" id="dp-track"></div></div>
  <div class="dp-nav">
    <button class="dp-btn" id="dp-prev" onclick="go(-1)" disabled>←</button>
    <span class="dp-cnt" id="dp-cnt"></span>
    <button class="dp-btn" id="dp-next" onclick="go(1)">→</button>
  </div>
</div>

<script>{js}</script>
</body>
</html>"""


def generate_index(dates):
    items = "".join(
        f'<a class="idx-a" href="{d}.html">'
        f'<span class="idx-date">{datetime.strptime(d,"%Y-%m-%d").strftime("%Y.%m.%d")}</span>'
        f'<span class="idx-dow">{["월","화","수","목","금","토","일"][datetime.strptime(d,"%Y-%m-%d").weekday()]}요일</span>'
        f'</a>'
        for d in sorted(dates, reverse=True)
    )
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>IT 카드뉴스 아카이브</title>
  <style>{CSS}
    .idx-wrap{{max-width:480px;margin:0 auto;padding:0 16px;display:flex;flex-direction:column;gap:10px;}}
    .idx-a{{display:flex;justify-content:space-between;align-items:center;background:#fff;
      border-radius:14px;padding:16px 20px;text-decoration:none;
      box-shadow:0 2px 14px rgba(109,40,217,.08);transition:background .15s;}}
    .idx-a:hover{{background:var(--acc-pale);}}
    .idx-date{{font-size:18px;font-weight:800;color:var(--dk);}}
    .idx-dow{{font-size:13px;color:var(--acc);font-weight:700;}}
  </style>
</head>
<body>
  <header class="ph">
    <p class="ph-chip">IT 카드뉴스</p>
    <h1 class="ph-date">아카이브</h1>
    <p class="ph-sub">지난 뉴스 모아보기</p>
  </header>
  <div class="idx-wrap">{items}</div>
</body>
</html>"""
