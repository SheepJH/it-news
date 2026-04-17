import anthropic
import json
import re

client = anthropic.Anthropic()

SYSTEM_PROMPT = """당신은 IT 뉴스를 한국 개발자/기술인을 위해 카드 뉴스로 정리하는 전문가입니다.
뉴스를 읽기 쉽고 임팩트 있게 한국어로 정리하세요.
반드시 유효한 JSON만 반환하고 다른 텍스트는 절대 포함하지 마세요."""

CLASSIFY_PROMPT = """다음 IT 뉴스 제목들을 분석해서 JSON 배열로 반환하세요.

뉴스 목록:
{stories}

각 뉴스마다 아래 형식으로 반환:
{{
  "index": 0,
  "type": "standard|versus|data|timeline|explainer",
  "category": "AI/ML|보안|개발|비즈니스|기타",
  "title_ko": "임팩트 있는 한국어 제목 (20자 내외)",
  "subtitle_ko": "부제목 (선택, 핵심 수치나 인용구 있으면 추가)",
  "summary": ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3"],
  "importance": "왜 중요한가 - 개발자/기술인 관점에서 2문장",
  "versus": null,
  "timeline": null,
  "stats": null
}}

타입 선택 기준:
- versus: 두 기술/제품/회사 명시적 비교 (A vs B)
- data: 수치/통계/순위 중심
- timeline: 사건 경과나 역사
- explainer: 개념/기술 설명, "what is", "how"
- standard: 그 외 일반 뉴스

versus 타입이면 versus 필드 채우기:
"versus": {{
  "a": {{"name": "이름", "pros": ["장점1", "장점2"], "cons": ["단점1"], "spec": "가격/성능 수치"}},
  "b": {{"name": "이름", "pros": ["장점1", "장점2"], "cons": ["단점1"], "spec": "가격/성능 수치"}},
  "verdict": "결론 한 줄"
}}

timeline 타입이면 timeline 필드 채우기:
"timeline": [{{"date": "날짜", "event": "사건"}}]

data 타입이면 stats 필드 채우기:
"stats": [{{"label": "라벨", "value": "수치", "unit": "단위"}}]

JSON 배열만 반환. 마크다운 코드블록 금지."""


def process_stories(stories):
    """스토리 목록을 Claude API로 처리하여 구조화된 카드 데이터 반환"""
    if not stories:
        return []

    stories_text = "\n".join(
        f"{i}. {s['title']} | 점수: {s['score']} | {s['url']}"
        for i, s in enumerate(stories)
    )

    prompt = CLASSIFY_PROMPT.format(stories=stories_text)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()

        # JSON 배열 추출 (혹시 코드블록이 붙어있으면 제거)
        raw = re.sub(r"```json|```", "", raw).strip()
        cards = json.loads(raw)

        # 원문 URL 붙이기
        for card in cards:
            idx = card.get("index", 0)
            if 0 <= idx < len(stories):
                card["url"] = stories[idx]["url"]
                card["hn_url"] = stories[idx]["hn_url"]
                card["score"] = stories[idx]["score"]
                card["comments"] = stories[idx]["comments"]

        print(f"[claude] {len(cards)}개 카드 처리 완료")
        return cards

    except json.JSONDecodeError as e:
        print(f"[claude] JSON 파싱 실패: {e}\n원본:\n{raw[:300]}")
        return []
    except Exception as e:
        print(f"[claude] API 호출 실패: {e}")
        return []


KEYWORD_PROMPT = """아래 오늘의 IT 뉴스 제목들을 보고, 등장하는 중요한 IT 용어/기술/개념 중
독자가 몰라서 찾아볼 만한 것 4~6개를 골라 JSON 배열로 반환하세요.

뉴스:
{stories}

형식:
[
  {{
    "term": "용어 원문 (영문 약어면 그대로, 한글이면 한글)",
    "full": "풀 네임 (약어인 경우에만, 아니면 null)",
    "desc": "한국어로 2문장 이내 설명. 이게 뭔지 + 왜 요즘 중요한지."
  }}
]

선택 기준:
- 뉴스에 실제로 등장하거나 관련된 핵심 기술 용어
- 일반인이 검색해볼 만한 것 (너무 기초적인 건 제외)
- 요즘 IT 흐름에서 자주 나오는 것 우선

JSON 배열만 반환. 마크다운 코드블록 금지."""


def extract_daily_keywords(stories):
    """오늘 뉴스 전체에서 중요 IT 용어 4~6개 추출"""
    if not stories:
        return []

    stories_text = "\n".join(f"- {s['title']}" for s in stories)
    prompt = KEYWORD_PROMPT.format(stories=stories_text)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = re.sub(r"```json|```", "", response.content[0].text.strip()).strip()
        keywords = json.loads(raw)
        print(f"[claude] 키워드 {len(keywords)}개 추출 완료")
        return keywords
    except Exception as e:
        print(f"[claude] 키워드 추출 실패: {e}")
        return []
