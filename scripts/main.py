import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

from fetch_news import fetch_top_stories
from claude_processor import generate_explainer_json
from renderer import render_card_set, generate_viewer_html, generate_index


def get_existing_dates():
    return sorted(p.stem for p in DOCS.glob("????-??-??.html"))


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'='*50}")
    print(f"  IT 카드뉴스 생성 시작 — {today}")
    print(f"{'='*50}\n")

    # 1. 뉴스 수집 (1개)
    stories = fetch_top_stories(count=1)
    if not stories:
        print("[main] 수집된 뉴스 없음. 종료.")
        sys.exit(1)

    # 2. Claude로 explainer 6페이지 JSON 생성
    data = generate_explainer_json(stories[0])
    if not data:
        print("[main] JSON 생성 실패. 종료.")
        sys.exit(1)

    # 3. PNG 렌더링 (커버에 날짜 주입)
    if data["pages"] and data["pages"][0].get("template") == "explainer_01_cover.html":
        data["pages"][0]["date"] = datetime.now().strftime("%Y.%m.%d")
    output_dir = DOCS / today
    png_paths = render_card_set(data, output_dir)

    # 4. 뷰어 HTML 생성
    viewer_html = generate_viewer_html(
        today, png_paths,
        source_url=stories[0]["url"],
        keywords=data.get("keywords"),
    )
    viewer_path = DOCS / f"{today}.html"
    viewer_path.write_text(viewer_html, encoding="utf-8")
    print(f"[main] 뷰어 저장: {viewer_path}")

    # 5. 인덱스 갱신
    all_dates = get_existing_dates()
    if today not in all_dates:
        all_dates.append(today)
    index_html = generate_index(all_dates)
    (DOCS / "index.html").write_text(index_html, encoding="utf-8")
    print("[main] 인덱스 갱신 완료")

    # 6. URL 출력 (슬랙 알림은 git push 후 워크플로우에서 별도 실행)
    github_repo = os.environ.get("GH_REPO", "")
    repo_name = github_repo.split("/")[-1] if "/" in github_repo else "it-news"
    github_user = github_repo.split("/")[0] if "/" in github_repo else ""
    page_url = f"https://{github_user}.github.io/{repo_name}/{today}.html"

    print(f"\n완료! → {page_url}\n")
    print(f"CARD_COUNT={len(png_paths)}")


if __name__ == "__main__":
    main()
