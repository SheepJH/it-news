"""
뉴스 1개 → explainer 6페이지 JSON 생성
"""
import json
import os
import anthropic

HANDLE = "it.daily"

SYSTEM_PROMPT = """당신은 IT/테크 뉴스를 한국어 인스타그램 카드뉴스로 변환하는 전문가입니다.
주어진 뉴스 기사를 분석해 6페이지짜리 explainer 카드뉴스 JSON을 생성하세요.

반환 형식은 반드시 아래 JSON 구조를 정확히 따르고, 설명 텍스트 없이 JSON만 출력하세요.

글자 수 제한 (반드시 준수):
- cover question: 최대 3줄, 줄당 7자 이하, \\n으로 줄바꿈
- definition headline_before_highlight + headline_highlight 합산: 각 줄 최대 10자
- definition body_text: 최대 3줄, 줄당 15자 이하
- comparison before_items: 각 항목 10자 이하, 최대 4개
- comparison after_chain: 각 항목 10자 이하, 최대 3개
- process steps.title: 12자 이하
- process steps.desc: 20자 이하
- example items.title: 15자 이하
- example items.desc: 20자 이하
- conclusion headline_parts: 각 part.text 8자 이하, 최대 4개
- 이모지 금지
- 원문 문장 복붙 금지, 반드시 재작성

JSON 구조:
{
  "genre": "explainer",
  "handle": "it.daily",
  "pages": [
    {
      "template": "explainer_01_cover.html",
      "section_label": "00 · 커버",
      "page_current": 1,
      "page_total": 6,
      "series_meta": "IT DAILY",
      "question": "줄1\\n줄2\\n줄3",
      "subtitle": "부제목\\n두번째줄"
    },
    {
      "template": "explainer_02_definition.html",
      "section_label": "01 · 정의",
      "page_current": 2,
      "page_total": 6,
      "label_top": "ONE-LINER",
      "headline_before_highlight": "앞부분\\n",
      "headline_highlight": "핵심단어",
      "body_text": "설명 첫줄\\n두번째줄\\n세번째줄"
    },
    {
      "template": "explainer_03_comparison.html",
      "section_label": "02 · 왜 필요해?",
      "page_current": 3,
      "page_total": 6,
      "headline": "비교 헤드라인",
      "before_label": "BEFORE",
      "before_items": ["항목1", "항목2", "항목3"],
      "before_note": "기존 문제점",
      "after_label": "AFTER",
      "after_chain": ["항목1", "핵심", "결과"],
      "after_note": "개선된 점"
    },
    {
      "template": "explainer_04_process.html",
      "section_label": "03 · 작동 원리",
      "page_current": 4,
      "page_total": 6,
      "headline": "3단계로 이해하기",
      "steps": [
        {"title": "단계 제목1", "desc": "단계 설명1"},
        {"title": "단계 제목2", "desc": "단계 설명2"},
        {"title": "단계 제목3", "desc": "단계 설명3"}
      ]
    },
    {
      "template": "explainer_05_example.html",
      "section_label": "04 · 실제 예시",
      "page_current": 5,
      "page_total": 6,
      "headline": "이미 쓰고 있는 곳",
      "items": [
        {"title": "사례 제목1", "desc": "사례 설명1", "tag": "LIVE"},
        {"title": "사례 제목2", "desc": "사례 설명2", "tag": "NEW"},
        {"title": "사례 제목3", "desc": "사례 설명3", "tag": "LIVE"}
      ]
    },
    {
      "template": "explainer_06_conclusion.html",
      "section_label": "05 · 한 줄 요약",
      "page_current": 6,
      "page_total": 6,
      "label_top": "REMEMBER THIS",
      "headline_parts": [
        {"text": "줄1", "highlight": false},
        {"text": "줄2", "highlight": true},
        {"text": "줄3", "highlight": false},
        {"text": "줄4", "highlight": false}
      ],
      "body_text": "핵심 메시지\\n두번째줄",
      "next_episode": "다음 편: 관련 주제"
    }
  ]
}"""


def generate_explainer_json(story: dict) -> dict:
    """뉴스 1개 → explainer 6페이지 JSON 생성"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    user_prompt = f"""다음 IT 뉴스를 6페이지 explainer 카드뉴스로 변환하세요.

제목: {story['title']}
URL: {story['url']}

글자 수 제한을 반드시 지키고, JSON만 출력하세요."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = response.content[0].text.strip()

    # JSON 블록 추출
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    data = json.loads(text)
    data["handle"] = HANDLE
    print(f"[claude] explainer JSON 생성 완료 ({len(data['pages'])}페이지)")
    return data
