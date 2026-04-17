"""
API 호출 없이 더미 데이터로 HTML 생성 후 브라우저로 열기
사용: python scripts/test_html.py
"""
import os, sys, webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_html import generate_page

DUMMY_CARDS = [
    {
        "type": "standard",
        "category": "AI/ML",
        "title_ko": "Claude Opus 4.7 드디어 출시",
        "subtitle_ko": "Anthropic의 최신 플래그십 모델 공개",
        "summary": [
            "Anthropic이 Claude Opus 4.7을 공식 발표, 기존 대비 성능 향상",
            "에이전틱 작업 및 복잡한 추론 능력 크게 강화",
            "HN 점수 1577로 이번 주 최고 화제작",
        ],
        "importance": "현재 가장 강력한 상용 AI 모델 중 하나로, 코딩·분석·에이전트 파이프라인 구축에 직접 영향. 경쟁 모델 대비 성능 벤치마크 확인 필요.",
        "url": "https://anthropic.com",
        "score": 1577, "comments": 1120,
    },
    {
        "type": "versus",
        "category": "AI/ML",
        "title_ko": "Claude 4 vs GPT-5, 뭐가 나을까?",
        "subtitle_ko": "코딩이면 Claude, 범용이면 GPT-5",
        "summary": ["코딩 특화 벤치마크 Claude 우세", "멀티모달은 GPT-5 강점", "가격은 비슷한 수준"],
        "importance": "개발자라면 용도에 따라 선택이 달라짐. 코딩 에이전트는 Claude, 이미지+텍스트 혼합 작업은 GPT-5.",
        "versus": {
            "a": {"name": "Claude 4", "pros": ["코딩 강함", "긴 문맥"], "cons": ["이미지 약함"], "spec": "$3 / 1M tokens"},
            "b": {"name": "GPT-5",   "pros": ["멀티모달",  "플러그인"], "cons": ["할루시네이션"], "spec": "$2.5 / 1M tokens"},
            "verdict": "코딩·에이전트면 Claude, 범용·이미지면 GPT-5",
        },
        "url": "https://openai.com",
        "score": 973, "comments": 640,
    },
    {
        "type": "data",
        "category": "비즈니스",
        "title_ko": "국내 AI 스타트업 투자 급증",
        "subtitle_ko": "전년 대비 138% 증가, 아시아 3위",
        "summary": ["2026년 국내 AI 투자 $3.1B 돌파", "신규 설립 스타트업 82개사", "정부 지원 정책 확대 영향"],
        "importance": "AI 인프라·툴링 분야 창업 기회 확대. 개발자 수요도 함께 폭증 중.",
        "stats": [
            {"label": "YoY 증가", "value": "+138", "unit": "%"},
            {"label": "아시아 순위", "value": "#3", "unit": ""},
            {"label": "신규 설립", "value": "82", "unit": "개"},
        ],
        "url": "https://techcrunch.com",
        "score": 540, "comments": 280,
    },
    {
        "type": "timeline",
        "category": "보안",
        "title_ko": "SKT 해킹 사건 타임라인",
        "subtitle_ko": "고객 데이터 유출 경과",
        "summary": ["최초 침입부터 공개까지 7일 소요", "일부 고객 데이터 유출 확인", "정부 조사 착수"],
        "importance": "통신사 보안 사고는 파급력이 크다. USIM 재발급 및 비밀번호 변경 권장.",
        "timeline": [
            {"date": "04.10", "event": "최초 침입 감지"},
            {"date": "04.12", "event": "고객 데이터 일부 유출"},
            {"date": "04.15", "event": "SKT 공식 인정 발표"},
            {"date": "04.17", "event": "정부 조사 착수 ← 현재"},
        ],
        "url": "https://zdnet.co.kr",
        "score": 820, "comments": 430,
    },
    {
        "type": "explainer",
        "category": "개발",
        "title_ko": "MCP가 뭔데 다들 난리야?",
        "subtitle_ko": "AI가 외부 도구에 접근하게 해주는 표준 규격",
        "summary": ["USB 포트처럼 AI와 외부 도구를 연결하는 표준", "Claude, GPT 모두 지원 중", "한 번 구현하면 모든 AI에서 재사용 가능"],
        "importance": "MCP를 알면 AI 자동화 도구를 직접 만들 수 있다. 개발자 생산성 도구 시장의 새 표준이 될 것.",
        "url": "https://modelcontextprotocol.io",
        "score": 1100, "comments": 760,
    },
]

DUMMY_KEYWORDS = [
    {"term": "MCP",         "full": "Model Context Protocol", "desc": "AI가 외부 파일·DB·API에 접근하게 해주는 표준 규격. USB 포트처럼 한 번 만들면 어떤 AI든 연결 가능."},
    {"term": "에이전틱 AI", "full": None,                     "desc": "사람 개입 없이 AI가 스스로 계획·실행·판단하는 방식. 코딩 자동화, 리서치 자동화 등에 활용."},
    {"term": "RAG",         "full": "Retrieval-Augmented Generation", "desc": "AI가 실시간으로 외부 데이터를 검색해 답변하는 기법. 환각(hallucination)을 줄이는 핵심 기술."},
    {"term": "Fine-tuning", "full": None,                     "desc": "기존 AI 모델을 특정 도메인 데이터로 추가 학습시키는 것. 의료·법률 등 전문 분야에 많이 쓰임."},
]

if __name__ == "__main__":
    html = generate_page(
        DUMMY_CARDS,
        date_str="2026-04-17",
        keywords=DUMMY_KEYWORDS,
        prev_date="2026-04-16",
        next_date=None,
    )

    out = Path(__file__).parent.parent / "docs" / "_test.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"생성 완료 → {out}")
    webbrowser.open(f"file://{out}")
