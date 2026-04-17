import requests
import xml.etree.ElementTree as ET
import random

# RSS 피드 소스 (카테고리별로 분산)
RSS_FEEDS = [
    # AI/ML
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "AI/ML"},
    # 개발/오픈소스
    {"url": "https://github.blog/feed/",                                      "category": "개발"},
    # 보안
    {"url": "https://feeds.feedburner.com/TheHackersNews",                    "category": "보안"},
    # 비즈니스/스타트업
    {"url": "https://techcrunch.com/category/startups/feed/",                 "category": "비즈니스"},
    # 기술 전반
    {"url": "https://www.theverge.com/rss/index.xml",                         "category": "기타"},
    # 개발자
    {"url": "https://feeds.feedburner.com/TechCrunch",                        "category": "개발"},
]

IT_KEYWORDS = [
    "ai", "gpt", "llm", "claude", "openai", "google", "microsoft", "apple",
    "python", "javascript", "react", "rust", "golang", "linux", "docker",
    "cloud", "aws", "azure", "kubernetes", "api", "startup", "funding",
    "security", "hack", "breach", "data", "model", "agent", "open source",
    "github", "developer", "software", "hardware", "chip", "quantum",
    "robotics", "autonomous", "blockchain", "crypto", "tool", "release",
]

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
}


def _parse_feed(feed_url):
    """RSS/Atom 피드 파싱 → [{title, url, category}] 반환"""
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


def fetch_top_stories(count=5):
    """RSS 피드에서 카테고리 분산하여 IT 뉴스 count개 반환"""
    # 각 피드에서 후보 수집
    pool = []  # [{title, url, category}]
    seen_urls = set()

    for feed in RSS_FEEDS:
        articles = _parse_feed(feed["url"])
        for a in articles:
            url = a["url"]
            title = a["title"]
            if url in seen_urls:
                continue
            if not any(kw in title.lower() for kw in IT_KEYWORDS):
                continue
            seen_urls.add(url)
            pool.append({"title": title, "url": url, "category": feed["category"],
                         "score": 0, "comments": 0, "hn_url": url})

    if not pool:
        print("[fetch] 수집된 뉴스 없음")
        return []

    # 카테고리별로 최대 2개씩 균등 선택
    by_cat = {}
    for item in pool:
        by_cat.setdefault(item["category"], []).append(item)

    selected = []
    # 라운드로빈 방식으로 카테고리 균등 선택
    cats = list(by_cat.keys())
    random.shuffle(cats)
    i = 0
    cat_counts = {c: 0 for c in cats}
    MAX_PER_CAT = 2

    for item in pool:
        if len(selected) >= count:
            break
        cat = item["category"]
        if cat_counts[cat] < MAX_PER_CAT:
            selected.append(item)
            cat_counts[cat] += 1

    # 부족하면 나머지에서 채우기
    if len(selected) < count:
        for item in pool:
            if len(selected) >= count:
                break
            if item not in selected:
                selected.append(item)

    print(f"[fetch] {len(selected)}개 뉴스 수집 완료 (카테고리: {dict(cat_counts)})")
    return selected[:count]
