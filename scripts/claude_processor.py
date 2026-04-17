import anthropic
import json
import re

client = anthropic.Anthropic()

SYSTEM_PROMPT = """당신은 IT 뉴스를 한국 개발자/기술인을 위한 인스타그램 카드뉴스로 만드는 전문가입니다.
각 슬라이드는 독립적으로 읽혀야 하며, 구체적 수치와 사실에 기반해야 합니다.
반드시 유효한 JSON만 반환하세요. 마크다운 코드블록 금지."""

CLASSIFY_PROMPT = """다음 IT 뉴스 제목들을 분석하여 카드뉴스용 JSON 배열로 반환하세요.

뉴스 목록:
{stories}

각 뉴스마다 아래 형식으로 반환하세요:
{{
  "index": 0,
  "type": "standard|versus|data|timeline|explainer",
  "category": "AI/ML|보안|개발|비즈니스|기타",
  "title_ko": "강렬한 한국어 제목. 20자 이내. 숫자나 강한 동사 우선.",
  "subtitle_ko": "핵심 수치 또는 임팩트 있는 한 줄. 없으면 null.",
  "points": [
    "첫 번째 핵심 사실. 이 슬라이드 하나에 집중할 독립적 내용. 구체적 수치·사실 반드시 포함. 완결된 2문장.",
    "두 번째 핵심 사실. 첫 번째와 다른 각도. 독립적으로 읽혀야 함. 구체적 수치 포함. 2문장.",
    "세 번째 핵심 사실. 맥락·배경·영향 중심. 독립적으로 읽혀야 함. 2문장."
  ],
  "importance": "왜 지금 이게 중요한가. 개발자/IT인 관점. 임팩트 있게. 2-3문장.",
  "takeaway": "독자가 지금 당장 알거나 해야 할 것. 행동 지향적. 구체적. 1-2문장.",
  "versus": null,
  "timeline": null,
  "stats": null
}}

타입 선택 기준:
- versus: A vs B 명시적 비교 (두 기술·제품·회사)
- data: 수치·통계·순위 중심 뉴스
- timeline: 사건 경과·역사적 흐름
- explainer: 개념·기술 설명 ("what is", "how it works")
- standard: 그 외

versus 타입이면 versus 필드 채우기:
"versus": {{
  "a": {{
    "name": "A 이름",
    "highlight": "A의 핵심 특징. 구체적 수치 포함. 독립 슬라이드용 2-3문장.",
    "pros": ["장점1 (수치 포함)", "장점2"],
    "cons": ["단점1"],
    "spec": "가격·성능 핵심 수치 한 줄"
  }},
  "b": {{
    "name": "B 이름",
    "highlight": "B의 핵심 특징. 구체적 수치 포함. 독립 슬라이드용 2-3문장.",
    "pros": ["장점1 (수치 포함)", "장점2"],
    "cons": ["단점1"],
    "spec": "가격·성능 핵심 수치 한 줄"
  }},
  "verdict": "어떤 상황에 무엇이 더 나은지. 구체적으로. 2문장."
}}

timeline 타입이면 timeline 필드 채우기 (날짜순, 최신이 마지막):
"timeline": [{{"date": "날짜", "event": "구체적 사건 설명"}}]

data 타입이면 stats 필드 채우기 (가장 임팩트 있는 수치 3개):
"stats": [{{"label": "무엇을 나타내는 수치인지", "value": "수치", "unit": "단위"}}]

JSON 배열만 반환."""


def process_stories(stories):
    if not stories:
        return []

    stories_text = "\n".join(
        f"{i}. {s['title']} | HN점수: {s['score']} | {s['url']}"
        for i, s in enumerate(stories)
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=5000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": CLASSIFY_PROMPT.format(stories=stories_text)}],
        )
        raw = re.sub(r"```json|```", "", response.content[0].text.strip()).strip()
        cards = json.loads(raw)

        for card in cards:
            idx = card.get("index", 0)
            if 0 <= idx < len(stories):
                card["url"]      = stories[idx]["url"]
                card["hn_url"]   = stories[idx]["hn_url"]
                card["score"]    = stories[idx]["score"]
                card["comments"] = stories[idx]["comments"]

        print(f"[claude] {len(cards)}개 카드 처리 완료")
        return cards

    except json.JSONDecodeError as e:
        print(f"[claude] JSON 파싱 실패: {e}")
        return []
    except Exception as e:
        print(f"[claude] API 호출 실패: {e}")
        return []


KEYWORD_PROMPT = """아래 오늘의 IT 뉴스들을 보고, 독자가 모를 만한 핵심 IT 용어·기술 4~6개를
JSON 배열로 반환하세요.

뉴스:
{stories}

형식:
[{{
  "term": "용어 (영문 약어면 그대로)",
  "full": "풀네임 (약어일 때만, 아니면 null)",
  "desc": "이게 뭔지 + 왜 요즘 중요한지. 한국어 2문장."
}}]

기준: 뉴스에 실제 등장, 일반인이 찾아볼 만한 것, 기초 용어 제외.
JSON 배열만 반환."""


def extract_daily_keywords(stories):
    if not stories:
        return []

    stories_text = "\n".join(f"- {s['title']}" for s in stories)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": KEYWORD_PROMPT.format(stories=stories_text)}],
        )
        raw = re.sub(r"```json|```", "", response.content[0].text.strip()).strip()
        keywords = json.loads(raw)
        print(f"[claude] 키워드 {len(keywords)}개 추출 완료")
        return keywords
    except Exception as e:
        print(f"[claude] 키워드 추출 실패: {e}")
        return []
