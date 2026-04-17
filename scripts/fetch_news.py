import json
import requests
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).parent.parent
USED_URLS_FILE = ROOT / "docs" / "used_urls.json"

HN_TOP_URL    = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL   = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# 상위 몇 개 스토리를 후보로 볼지
HN_CANDIDATE_COUNT = 50

IT_KEYWORDS = [
    "ai", "gpt", "llm", "claude", "openai", "google", "microsoft", "apple",
    "python", "javascript", "react", "rust", "golang", "linux", "docker",
    "cloud", "aws", "azure", "kubernetes", "api", "startup", "funding",
    "security", "hack", "breach", "model", "agent", "open source",
    "github", "developer", "software", "hardware", "chip", "quantum",
    "robotics", "autonomous", "blockchain", "crypto", "release",
]


def _load_used_urls() -> dict:
    if USED_URLS_FILE.exists():
        data = json.loads(USED_URLS_FILE.read_text())
        # 구버전 호환 (list → dict)
        if isinstance(data, list):
            return {url: "2000-01-01" for url in data}
        return data
    return {}


def _save_used_url(url: str):
    used = _load_used_urls()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    used[url] = today
    # 90일 이상 된 항목 정리
    cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
    used = {u: d for u, d in used.items() if d >= cutoff}
    USED_URLS_FILE.parent.mkdir(exist_ok=True)
    USED_URLS_FILE.write_text(json.dumps(used, ensure_ascii=False, indent=2))


def _fetch_item(story_id: int):
    try:
        resp = requests.get(HN_ITEM_URL.format(story_id), timeout=5)
        return resp.json()
    except Exception:
        return None


def fetch_top_stories(count: int = 1) -> list:
    """
    HN 상위 스토리 → 점수순 정렬 → 24시간 이내 + 키워드 + 미사용 첫 번째 반환
    """
    used_urls = set(_load_used_urls().keys())
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    # 상위 N개 ID 가져오기
    try:
        top_ids = requests.get(HN_TOP_URL, timeout=10).json()[:HN_CANDIDATE_COUNT]
    except Exception as e:
        print(f"[fetch] HN 상위 스토리 목록 실패: {e}")
        return []

    print(f"[fetch] HN 상위 {len(top_ids)}개 스토리 조회 중...")

    # 병렬로 스토리 상세 조회
    stories = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_fetch_item, sid): sid for sid in top_ids}
        for future in as_completed(futures):
            item = future.result()
            if item and item.get("type") == "story" and item.get("url"):
                stories.append(item)

    # 점수 높은 순 정렬
    stories.sort(key=lambda x: x.get("score", 0), reverse=True)
    print(f"[fetch] 유효 스토리 {len(stories)}개 (점수순 정렬)")

    for item in stories:
        url   = item["url"]
        title = item["title"]
        score = item.get("score", 0)
        pub   = datetime.fromtimestamp(item["time"], tz=timezone.utc)

        # 24시간 초과 제외
        if pub < cutoff:
            continue

        # 중복 제외
        if url in used_urls:
            print(f"[fetch] 중복 건너뜀: {title[:40]}")
            continue

        # 키워드 필터
        if not any(kw in title.lower() for kw in IT_KEYWORDS):
            continue

        _save_used_url(url)
        print(f"[fetch] 선택: {title} (점수 {score})")
        return [{"title": title, "url": url, "score": score}]

    print("[fetch] 조건에 맞는 기사 없음")
    return []
