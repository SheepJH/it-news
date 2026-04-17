import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 프로젝트 루트 기준 경로
ROOT  = Path(__file__).parent.parent
DOCS  = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

from fetch_news       import fetch_top_stories
from claude_processor import process_stories, extract_daily_keywords
from generate_html    import generate_page, generate_index
from kakao_notify     import send_daily_card


def get_existing_dates():
    return sorted(
        p.stem for p in DOCS.glob("????-??-??.html")
    )


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'='*50}")
    print(f"  IT 카드뉴스 생성 시작 — {today}")
    print(f"{'='*50}\n")

    # 1. 뉴스 수집
    stories = fetch_top_stories(count=5)
    if not stories:
        print("[main] 수집된 뉴스 없음. 종료.")
        sys.exit(1)

    # 2. Claude로 처리 (카드 + 키워드 병렬 느낌으로 순차 호출)
    cards = process_stories(stories)
    if not cards:
        print("[main] 카드 생성 실패. 종료.")
        sys.exit(1)

    keywords = extract_daily_keywords(stories)

    # 3. 날짜 목록 (이전/다음 내비게이션용)
    dates = get_existing_dates()
    prev_date = dates[-1] if dates else None
    next_date = None  # 오늘이 최신

    # 4. HTML 페이지 생성
    html = generate_page(cards, today, keywords=keywords, prev_date=prev_date, next_date=next_date)
    out_path = DOCS / f"{today}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"[main] 페이지 저장: {out_path}")

    # 이전 날짜 페이지의 next_date 업데이트
    if prev_date:
        prev_path = DOCS / f"{prev_date}.html"
        if prev_path.exists():
            prev_html = generate_page(
                [],           # 카드는 재생성 안 함 (기존 파일 수정은 복잡하므로 간단히 처리)
                prev_date,
                next_date=today
            )
            # 실제로는 기존 prev 페이지에서 next 링크만 바꾸면 되지만
            # 간단히 전체 재생성하지 않고 sed-like 치환으로 처리
            content = prev_path.read_text(encoding="utf-8")
            content = content.replace(
                '<span class="nav-btn disabled">다음 →</span>',
                f'<a class="nav-btn" href="{today}.html">{today} →</a>'
            )
            prev_path.write_text(content, encoding="utf-8")
            print(f"[main] 이전 페이지 next 링크 업데이트: {prev_date}")

    # 5. 인덱스 페이지 갱신
    all_dates = dates + [today]
    index_html = generate_index(all_dates)
    (DOCS / "index.html").write_text(index_html, encoding="utf-8")
    print("[main] 인덱스 페이지 갱신 완료")

    # 6. 카카오톡 알림
    github_repo  = os.environ.get("GITHUB_REPO", "")
    # GitHub Pages URL: https://<user>.github.io/<repo>/YYYY-MM-DD.html
    repo_name = github_repo.split("/")[-1] if "/" in github_repo else "it-news"
    github_user = github_repo.split("/")[0] if "/" in github_repo else ""
    page_url = f"https://{github_user}.github.io/{repo_name}/{today}.html"

    send_daily_card(today, page_url, card_count=len(cards))

    print(f"\n✅ 완료! → {page_url}\n")


if __name__ == "__main__":
    main()
