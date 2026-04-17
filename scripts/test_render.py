"""
API 비용 없이 렌더러 로컬 테스트용.
고정 JSON으로 PNG + 뷰어 HTML 생성.
실행: cd scripts && python test_render.py
"""
from pathlib import Path
from renderer import render_card_set, generate_viewer_html

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

MOCK_DATA = {
    "genre": "explainer",
    "keywords": [
        {"term": "Claude Opus 4.7", "definition": "Anthropic이 공개한 최신 플래그십 AI 모델"},
        {"term": "확장 사고", "definition": "복잡한 문제를 단계별로 추론하는 AI 기능"},
        {"term": "컴퓨터 사용", "definition": "AI가 직접 화면을 보고 마우스·키보드를 조작하는 기능"},
    ],
    "pages": [
        {
            "template": "explainer_01_cover.html",
            "section_label": "커버",
            "page_current": 1,
            "page_total": 7,
            "date": "2026.04.17",
            "question": "Claude\nOpus 4.7\n뭐가 달라?",
            "subtitle": "Anthropic 최신 모델\n핵심 변화 정리",
        },
        {
            "template": "explainer_02_definition.html",
            "section_label": "정의",
            "page_current": 2,
            "page_total": 7,
            "label_top": "ONE-LINER",
            "headline_before_highlight": "생각하고\n행동하는\n",
            "headline_highlight": "AI 에이전트",
            "body_text": "단순 답변을 넘어\n스스로 계획하고\n실행까지 한다",
        },
        {
            "template": "explainer_03_comparison.html",
            "section_label": "무엇이 달라졌나",
            "page_current": 3,
            "page_total": 7,
            "headline": "Opus 4 vs Opus 4.7",
            "before_label": "OPUS 4",
            "before_items": ["텍스트 응답 중심", "도구 사용 제한적", "긴 추론 불안정"],
            "before_note": "강력하지만 에이전트엔 부족",
            "after_label": "OPUS 4.7",
            "after_chain": ["확장 사고 강화", "컴퓨터 직접 조작", "장시간 작업 안정"],
            "after_note": "에이전트 작업에 최적화",
        },
        {
            "template": "explainer_pros_cons.html",
            "section_label": "장단점",
            "page_current": 4,
            "page_total": 7,
            "headline": "솔직한 평가",
            "pros_label": "장점",
            "pros": ["에이전트 성능 압도적", "코딩·분석 정확도 향상", "긴 컨텍스트 처리"],
            "cons_label": "단점",
            "cons": ["여전히 비싼 API 비용", "응답 속도 느림", "Sonnet 대비 과스펙"],
        },
        {
            "template": "explainer_myth_fact.html",
            "section_label": "오해와 사실",
            "page_current": 5,
            "page_total": 7,
            "headline": "잘못 알려진 것들",
            "items": [
                {
                    "myth": "Opus 4.7이 GPT-5보다 무조건 낫다",
                    "fact": "용도에 따라 다름. 코딩·에이전트는 우위",
                },
                {
                    "myth": "무료로 쓸 수 있다",
                    "fact": "API는 유료. Claude.ai 일부 플랜만 접근 가능",
                },
            ],
        },
        {
            "template": "explainer_impact.html",
            "section_label": "파급 효과",
            "page_current": 6,
            "page_total": 7,
            "headline": "누가 영향받나",
            "impacts": [
                {"area": "개발자", "desc": "AI 에이전트로 반복 작업 자동화 가속"},
                {"area": "기업", "desc": "고비용 모델 도입 ROI 재검토 필요"},
                {"area": "경쟁사", "desc": "OpenAI·Google 차기 모델 출시 압박"},
            ],
        },
        {
            "template": "explainer_06_conclusion.html",
            "section_label": "마무리",
            "page_current": 7,
            "page_total": 7,
            "label_top": "REMEMBER THIS",
            "headline_parts": [
                {"text": "AI는 이제", "highlight": False},
                {"text": "답하는 것을", "highlight": False},
                {"text": "넘어섰다", "highlight": True},
            ],
            "body_text": "Opus 4.7은 에이전트 시대의\n본격적인 시작을 알린다",
        },
    ],
}

if __name__ == "__main__":
    date_str = "_test"
    output_dir = DOCS / date_str
    png_paths = render_card_set(MOCK_DATA, output_dir)

    viewer_html = generate_viewer_html(
        date_str, png_paths,
        source_url="https://www.anthropic.com/news/claude-opus-4-7",
        keywords=MOCK_DATA["keywords"],
    )
    viewer_path = DOCS / f"{date_str}.html"
    viewer_path.write_text(viewer_html, encoding="utf-8")
    print(f"\n뷰어 열기: open {viewer_path}")
