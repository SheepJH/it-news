import requests
import xml.etree.ElementTree as ET

# RSS 피드 소스
RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://github.blog/feed/",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://techcrunch.com/category/startups/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.feedburner.com/TechCrunch",
]

IT_KEYWORDS = [
    "ai", "gpt", "llm", "claude", "openai", "google", "microsoft", "apple",
    "python", "javascript", "react", "rust", "golang", "linux", "docker",
    "cloud", "aws", "azure", "kubernetes", "api", "startup", "funding",
    "security", "hack", "breach", "data", "model", "agent", "open source",
    "github", "developer", "software", "hardware", "chip", "quantum",
    "robotics", "autonomous", "blockchain", "crypto", "tool", "release",
]


def _parse_feed(feed_url):
    """RSS/Atom 피드 파싱 → [{title, url}] 반환"""
    try:
        resp = requests.get(feed_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
    except Exception as e:
        print(f"[fetch] RSS 파싱 실패 ({feed_url}): {e}")
        return []

    items = []
    # RSS 2.0
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link")  or "").strip()
        if title and link:
            items.append({"title": title, "url": link})
    # Atom
    if not items:
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title = (entry.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            link = (link_el.get("href") or "") if link_el is not None else ""
            if title and link:
                items.append({"title": title, "url": link})
    return items


def fetch_top_stories(count=1):
    """RSS 피드에서 IT 키워드 포함 기사 중 첫 번째 반환"""
    seen_urls = set()

    for feed_url in RSS_FEEDS:
        articles = _parse_feed(feed_url)
        for a in articles:
            url = a["url"]
            title = a["title"]
            if url in seen_urls:
                continue
            if not any(kw in title.lower() for kw in IT_KEYWORDS):
                continue
            seen_urls.add(url)
            story = {"title": title, "url": url, "score": 0, "comments": 0, "hn_url": url}
            print(f"[fetch] 선택: {title}")
            return [story]

    print("[fetch] 수집된 뉴스 없음")
    return []
