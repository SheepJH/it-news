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
        {"term": "ICE", "definition": "미국 이민관세집행국. 불법 이민 단속·추방 담당"},
        {"term": "Sensorvault", "definition": "구글이 운영하는 사용자 위치 기록 데이터베이스"},
        {"term": "지오펜스 영장", "definition": "특정 지역·시간대 내 기기 정보를 요청하는 수사 영장"},
    ],
    "pages": [
        {
            "template": "explainer_01_cover.html",
            "section_label": "커버",
            "page_current": 1,
            "page_total": 7,
            "series_meta": "IT DAILY",
            "date": "2026.04.15",
            "question": "구글이\n내 정보를\n팔았다?",
            "subtitle": "ICE에 넘어간 데이터\n무슨 일이 있었나",
        },
        {
            "template": "explainer_02_definition.html",
            "section_label": "정의",
            "page_current": 2,
            "page_total": 7,
            "label_top": "ONE-LINER",
            "headline_before_highlight": "약속을 깬\n",
            "headline_highlight": "구글의 선택",
            "body_text": "위치 데이터를 익명화\n하겠다더니 결국\nICE에 제공했다",
        },
        {
            "template": "explainer_timeline.html",
            "section_label": "타임라인",
            "page_current": 3,
            "page_total": 7,
            "headline": "어떻게 된 일인가",
            "events": [
                {"date": "2023", "event": "구글, 위치정보 익명화 약속"},
                {"date": "2024", "event": "Sensorvault 데이터 보존"},
                {"date": "2025.01", "event": "ICE에 데이터 제공 요청"},
                {"date": "2025.06", "event": "구글 요청 수락·전달"},
                {"date": "2026.04", "event": "EFF 폭로·논란 확산"},
            ],
        },
        {
            "template": "explainer_03_comparison.html",
            "section_label": "무엇이 달라졌나",
            "page_current": 4,
            "page_total": 7,
            "headline": "약속 전 vs 약속 후",
            "before_label": "약속",
            "before_items": ["위치 익명화", "보관 최소화", "제3자 차단"],
            "before_note": "2023년 구글의 공식 발표",
            "after_label": "현실",
            "after_chain": ["데이터 보존", "ICE 요청", "그대로 제공"],
            "after_note": "약속과 정반대 행동",
        },
        {
            "template": "explainer_stats.html",
            "section_label": "숫자로 보기",
            "page_current": 5,
            "page_total": 7,
            "headline": "사건의 규모",
            "stats": [
                {"value": "180개국", "label": "구글 위치추적", "note": "Sensorvault 범위"},
                {"value": "수억 건", "label": "보관 기록", "note": "익명화 전 원본"},
                {"value": "1년+", "label": "데이터 제공", "note": "ICE 협력 기간"},
            ],
        },
        {
            "template": "explainer_faq.html",
            "section_label": "자주 묻는 질문",
            "page_current": 6,
            "page_total": 7,
            "headline": "Q&A",
            "faqs": [
                {"q": "나도 해당되나?", "a": "구글 계정·위치 켠 적 있으면 잠재 대상"},
                {"q": "막을 방법은?", "a": "위치 기록 끄기·계정 데이터 삭제 설정"},
            ],
        },
        {
            "template": "explainer_06_conclusion.html",
            "section_label": "마무리",
            "page_current": 7,
            "page_total": 7,
            "label_top": "REMEMBER THIS",
            "headline_parts": [
                {"text": "무료 서비스의", "highlight": False},
                {"text": "진짜 비용은", "highlight": True},
                {"text": "내 데이터다", "highlight": False},
            ],
            "body_text": "약속은 바뀔 수 있다\n데이터는 한번 주면 못 돌린다",
        },
    ],
}

if __name__ == "__main__":
    date_str = "_test"
    output_dir = DOCS / date_str
    png_paths = render_card_set(MOCK_DATA, output_dir)

    viewer_html = generate_viewer_html(
        date_str, png_paths,
        source_url="https://www.eff.org/deeplinks/2026/04/google-broke-its-promise-me-now-ice-has-my-data",
        keywords=MOCK_DATA["keywords"],
    )
    viewer_path = DOCS / f"{date_str}.html"
    viewer_path.write_text(viewer_html, encoding="utf-8")
    print(f"\n뷰어 열기: open {viewer_path}")
