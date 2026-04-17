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
    """6개 PNG 생성, 경로 목록 반환"""
    output_dir.mkdir(parents=True, exist_ok=True)
    handle = data["handle"]
    pages = data["pages"]
    png_paths = []

    print(f"[renderer] {len(pages)}개 카드 렌더링 시작")

    for i, page_data in enumerate(pages, 1):
        page_copy = dict(page_data)
        template_name = page_copy.pop("template")
        context = {**page_copy, "handle": handle}

        print(f"  [{i}/{len(pages)}] {template_name}")
        html = _render_html(template_name, context)

        output_path = output_dir / f"card_{i:02d}.png"
        _html_to_png(html, output_path)
        png_paths.append(output_path)
        print(f"      → {output_path}")

    print(f"[renderer] 완료: {output_dir}/")
    return png_paths


def generate_viewer_html(date_str: str, png_paths: list) -> str:
    """docs/YYYY-MM-DD.html 뷰어 (img 태그 6장 나열)"""
    img_tags = "\n".join(
        f'    <img src="{date_str}/card_{i:02d}.png" alt="card {i}" style="width:100%;max-width:1080px;display:block;margin:0 auto 16px;">'
        for i in range(1, len(png_paths) + 1)
    )
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT 카드뉴스 — {date_str}</title>
<style>
  body {{ margin: 0; background: #111; padding: 24px 0; }}
  a.back {{ display: block; text-align: center; color: #aaa; font-family: sans-serif; margin-bottom: 24px; text-decoration: none; }}
</style>
</head>
<body>
  <a class="back" href="index.html">← 목록으로</a>
{img_tags}
</body>
</html>"""


def generate_index(dates: list) -> str:
    """docs/index.html — 날짜 목록"""
    items = "\n".join(
        f'    <li><a href="{d}.html">{d}</a></li>'
        for d in sorted(dates, reverse=True)
    )
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT 카드뉴스</title>
<style>
  body {{ font-family: sans-serif; background: #111; color: #eee; max-width: 600px; margin: 48px auto; padding: 0 24px; }}
  h1 {{ font-size: 1.4rem; margin-bottom: 24px; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin-bottom: 12px; }}
  a {{ color: #FFE566; text-decoration: none; font-size: 1.1rem; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
  <h1>IT 카드뉴스</h1>
  <ul>
{items}
  </ul>
</body>
</html>"""
