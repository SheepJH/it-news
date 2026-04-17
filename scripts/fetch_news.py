import requests

ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"

IT_KEYWORDS = [
    "ai", "gpt", "llm", "claude", "openai", "google", "microsoft", "apple",
    "python", "javascript", "react", "rust", "golang", "linux", "docker",
    "cloud", "aws", "azure", "kubernetes", "api", "startup", "funding",
    "security", "hack", "breach", "data", "model", "agent", "open source",
    "github", "developer", "software", "hardware", "chip", "quantum",
    "robotics", "autonomous", "blockchain", "crypto",
]


def fetch_top_stories(count=5):
    """Algolia HN API로 오늘 상위 IT 뉴스 count개 반환"""
    try:
        resp = requests.get(ALGOLIA_URL, params={
            "tags": "front_page",
            "hitsPerPage": 50,
        }, timeout=10)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
    except Exception as e:
        print(f"[fetch] HN top stories 요청 실패: {e}")
        return []

    stories = []
    for item in hits:
        if len(stories) >= count:
            break

        url = item.get("url") or ""
        title = item.get("title") or ""
        if not url or not title:
            continue

        if not any(kw in title.lower() for kw in IT_KEYWORDS):
            continue

        stories.append({
            "title": title,
            "url": url,
            "score": item.get("points", 0),
            "comments": item.get("num_comments", 0),
            "by": item.get("author", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={item.get('objectID','')}",
        })

    print(f"[fetch] {len(stories)}개 뉴스 수집 완료")
    return stories
