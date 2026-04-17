"""
Jinja2 → HTML → Playwright → PNG
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = ROOT / "design" / "templates"


def _render_html(template_name: str, context: dict) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template(template_name)
    return template.render(**context)


def _html_to_png(html: str, output_path: Path) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        page.set_content(html, wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(output_path), full_page=False)
        browser.close()


def render_card_set(data: dict, output_dir: Path) -> list:
    """PNG 생성, 경로 목록 반환"""
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = data["pages"]
    png_paths = []

    print(f"[renderer] {len(pages)}개 카드 렌더링 시작")

    for i, page_data in enumerate(pages, 1):
        page_copy = dict(page_data)
        template_name = page_copy.pop("template")
        context = {**page_copy}

        print(f"  [{i}/{len(pages)}] {template_name}")
        html = _render_html(template_name, context)

        output_path = output_dir / f"card_{i:02d}.png"
        _html_to_png(html, output_path)
        png_paths.append(output_path)
        print(f"      → {output_path}")

    print(f"[renderer] 완료: {output_dir}/")
    return png_paths


def generate_viewer_html(date_str: str, png_paths: list, source_url: str = "", keywords: list = None, og_image_url: str = "") -> str:
    """docs/YYYY-MM-DD.html 뷰어 — 가로 스와이프 캐러셀 + 키워드 섹션"""
    slides = "\n".join(
        f'      <div class="slide"><img src="{date_str}/card_{i:02d}.png" alt="card {i}"></div>'
        for i in range(1, len(png_paths) + 1)
    )
    dots = "\n".join(
        f'      <span class="dot{" active" if i == 1 else ""}" data-index="{i - 1}"></span>'
        for i in range(1, len(png_paths) + 1)
    )
    source_btn = (
        f'<a class="source-link" href="{source_url}" target="_blank">원본 기사 보기 →</a>'
        if source_url else ""
    )
    keyword_items = ""
    if keywords:
        keyword_items = "\n".join(
            f'    <div class="kw-item"><span class="kw-term">{kw["term"]}</span><span class="kw-def">{kw["definition"]}</span></div>'
            for kw in keywords
        )
        keyword_section = f"""  <div class="keywords">
    <div class="kw-title">핵심 키워드</div>
{keyword_items}
  </div>"""
    else:
        keyword_section = ""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT 카드뉴스 — {date_str}</title>
<meta property="og:type" content="website">
<meta property="og:title" content="IT 카드뉴스 — {date_str}">
<meta property="og:image" content="{og_image_url or f'{date_str}/card_01.png'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_image_url or f'{date_str}/card_01.png'}">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #1a1a1a; font-family: sans-serif; overflow-y: auto; }}
  .wrap {{
    max-width: 480px; margin: 0 auto;
    background: #111;
    min-height: 100dvh;
  }}
  .topbar {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 20px;
  }}
  .topbar a.back {{ color: #aaa; text-decoration: none; font-size: 0.9rem; }}
  a.source-link {{
    color: #FFE566; text-decoration: none; font-size: 0.85rem; font-weight: 500;
  }}
  .carousel-wrap {{ width: 100%; aspect-ratio: 1; overflow: hidden; }}
  .carousel {{
    display: flex; width: 100%; height: 100%;
    overflow-x: scroll; scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }}
  .carousel::-webkit-scrollbar {{ display: none; }}
  .slide {{
    min-width: 100%; height: 100%;
    scroll-snap-align: start;
    display: flex; align-items: center; justify-content: center;
  }}
  .slide img {{ width: 100%; height: 100%; object-fit: cover; }}
  .dots {{
    display: flex; justify-content: center; gap: 7px;
    padding: 12px 0;
  }}
  .dot {{
    width: 7px; height: 7px; border-radius: 50%;
    background: #444; transition: background 0.2s; cursor: pointer;
  }}
  .dot.active {{ background: #FFE566; }}
  .keywords {{
    margin: 8px 20px 32px;
    border-top: 1px solid #2a2a2a;
    padding-top: 20px;
  }}
  .kw-title {{
    color: #666; font-size: 0.75rem; letter-spacing: 2px;
    margin-bottom: 14px;
  }}
  .kw-item {{
    display: flex; flex-direction: column; gap: 4px;
    margin-bottom: 16px;
  }}
  .kw-term {{
    color: #FFE566; font-size: 0.95rem; font-weight: 600;
  }}
  .kw-def {{
    color: #aaa; font-size: 0.85rem; line-height: 1.5;
  }}
</style>
</head>
<body>
  <div class="wrap">
  <div class="topbar">
    <a class="back" href="index.html">← 목록</a>
    {source_btn}
  </div>
  <div class="carousel-wrap">
    <div class="carousel" id="carousel">
{slides}
    </div>
  </div>
  <div class="dots" id="dots">
{dots}
  </div>
{keyword_section}
  </div>
  <script>
    const carousel = document.getElementById('carousel');
    const dots = document.querySelectorAll('.dot');
    carousel.addEventListener('scroll', () => {{
      const i = Math.round(carousel.scrollLeft / carousel.clientWidth);
      dots.forEach((d, j) => d.classList.toggle('active', i === j));
    }}, {{ passive: true }});
    dots.forEach((dot, i) => {{
      dot.addEventListener('click', () => {{
        carousel.scrollTo({{ left: carousel.clientWidth * i, behavior: 'smooth' }});
      }});
    }});
  </script>
</body>
</html>"""


def generate_index(dates: list) -> str:
    """docs/index.html — 날짜별 썸네일 그리드"""
    cards = "\n".join(
        f"""    <a class="card" href="{d}.html">
      <div class="thumb"><img src="{d}/card_01.png" alt="{d}" loading="lazy"></div>
      <div class="date">{d}</div>
    </a>"""
        for d in sorted(dates, reverse=True)
    )
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT 카드뉴스</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #111; color: #eee; font-family: sans-serif; padding: 24px 16px; }}
  h1 {{ font-size: 1.1rem; color: #FFE566; margin-bottom: 20px; letter-spacing: 1px; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }}
  @media (min-width: 600px) {{
    .grid {{ grid-template-columns: repeat(3, 1fr); }}
  }}
  .card {{
    text-decoration: none; color: inherit;
    background: #1a1a1a; border-radius: 10px; overflow: hidden;
    transition: transform 0.15s;
  }}
  .card:active {{ transform: scale(0.97); }}
  .thumb {{ aspect-ratio: 1; overflow: hidden; }}
  .thumb img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .date {{ font-size: 0.8rem; color: #aaa; padding: 8px 10px; }}
</style>
</head>
<body>
  <h1>IT DAILY</h1>
  <div class="grid">
{cards}
  </div>
</body>
</html>"""
