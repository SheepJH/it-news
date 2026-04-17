import os
import requests
import subprocess

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_SEND_URL  = "https://kapi.kakao.com/v2/api/talk/memo/default/send"


def _refresh_access_token(refresh_token, rest_api_key):
    """refresh_token으로 새 access_token 발급"""
    resp = requests.post(KAKAO_TOKEN_URL, data={
        "grant_type":    "refresh_token",
        "client_id":     rest_api_key,
        "refresh_token": refresh_token,
    })
    data = resp.json()
    if "access_token" not in data:
        raise RuntimeError(f"토큰 갱신 실패: {data}")

    new_access  = data["access_token"]
    new_refresh = data.get("refresh_token", refresh_token)  # 갱신 안 되면 기존 유지
    return new_access, new_refresh


def _update_github_secret(secret_name, secret_value, repo):
    """GitHub CLI로 시크릿 갱신 (GitHub Actions 환경에서만 작동)"""
    result = subprocess.run(
        ["gh", "secret", "set", secret_name, "--body", secret_value, "--repo", repo],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[kakao] 시크릿 갱신 실패 ({secret_name}): {result.stderr}")
    else:
        print(f"[kakao] 시크릿 갱신 완료: {secret_name}")


def send_daily_card(date_str, page_url, card_count=5):
    """카카오톡 나에게 보내기로 오늘의 카드뉴스 링크 전송"""
    access_token  = os.environ.get("KAKAO_ACCESS_TOKEN", "")
    refresh_token = os.environ.get("KAKAO_REFRESH_TOKEN", "")
    rest_api_key  = os.environ.get("KAKAO_REST_API_KEY", "")
    github_repo   = os.environ.get("GH_REPO", "")

    if not access_token and not refresh_token:
        print("[kakao] 토큰 없음, 알림 건너뜀")
        return

    # access_token 만료 시 refresh
    if refresh_token and rest_api_key:
        try:
            access_token, new_refresh = _refresh_access_token(refresh_token, rest_api_key)
            print("[kakao] 토큰 갱신 성공")
            if github_repo:
                _update_github_secret("KAKAO_ACCESS_TOKEN",  access_token,  github_repo)
                if new_refresh != refresh_token:
                    _update_github_secret("KAKAO_REFRESH_TOKEN", new_refresh, github_repo)
        except Exception as e:
            print(f"[kakao] 토큰 갱신 실패: {e}")

    # 메시지 전송
    template = {
        "object_type": "feed",
        "content": {
            "title":       f"📰 오늘의 IT 카드뉴스 — {date_str}",
            "description": f"오늘의 IT 핵심 뉴스 {card_count}선이 준비됐어요. 탭해서 확인하세요.",
            "image_url":   "https://via.placeholder.com/800x400/7C3AED/FFFFFF?text=IT+%EC%B9%B4%EB%93%9C%EB%89%B4%EC%8A%A4",
            "image_width":  800,
            "image_height": 400,
            "link": {
                "web_url":        page_url,
                "mobile_web_url": page_url,
            },
        },
        "buttons": [{
            "title": "카드 보러가기 →",
            "link": {
                "web_url":        page_url,
                "mobile_web_url": page_url,
            },
        }],
    }

    import json
    resp = requests.post(
        KAKAO_SEND_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        data={"template_object": json.dumps(template, ensure_ascii=False)},
    )
    result = resp.json()
    if result.get("result_code") == 0:
        print(f"[kakao] 전송 완료 → {page_url}")
    else:
        print(f"[kakao] 전송 실패: {result}")
