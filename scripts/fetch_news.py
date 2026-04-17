import requests
from datetime import datetime

HN_API = "https://hacker-news.firebaseio.com/v1"

IT_KEYWORDS = [
    "ai", "gpt", "llm", "claude", "openai", "google", "microsoft", "apple",
    "python", "javascript", "react", "rust", "golang", "linux", "docker",
    "cloud", "aws", "azure", "kubernetes", "api", "startup", "funding",
    "security", "hack", "breach", "data", "model", "agent", "open source",
    "github", "developer", "software", "hardware", "chip", "quantum",
    "robotics", "autonomous", "blockchain", "crypto",
]


def fetch_top_stories(count=5):
    """HackerNews 상위 스토리 중 IT 관련 뉴스 count개 반환"""
    try:
        ids = requests.get(f"{HN_API}/topstories.json", timeout=10).json()[:80]
    except Exception as e:
        print(f"[fetch] HN top stories 요청 실패: {e}")
        return []

    stories = []
    for story_id in ids:
        if len(stories) >= count:
            break
        try:
            item = requests.get(f"{HN_API}/item/{story_id}.json", timeout=8).json()
        except Exception:
            continue

        if not item or item.get("type") != "story" or not item.get("url"):
            continue

        title_lower = item["title"].lower()
        if not any(kw in title_lower for kw in IT_KEYWORDS):
            continue

        stories.append({
            "title": item["title"],
            "url": item["url"],
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "by": item.get("by", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={story_id}",
        })

    print(f"[fetch] {len(stories)}개 뉴스 수집 완료")
    return stories
