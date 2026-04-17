import os
import requests


def send_daily_card(date_str: str, page_url: str, card_count: int = 5, thumbnail_url: str = ""):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        print("[slack] SLACK_WEBHOOK_URL 없음, 건너뜀")
        return

    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*오늘의 IT 카드뉴스 — {date_str}*\n카드 {card_count}장 준비됐습니다.",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "보러가기"},
                    "url": page_url,
                },
            },
        ]
    }

    if thumbnail_url:
        payload["blocks"].append({
            "type": "image",
            "image_url": thumbnail_url,
            "alt_text": f"IT 카드뉴스 {date_str}",
        })

    resp = requests.post(webhook_url, json=payload)
    if resp.status_code == 200:
        print(f"[slack] 전송 완료 → {page_url}")
    else:
        print(f"[slack] 전송 실패: {resp.status_code} {resp.text}")


def send_error(date_str: str, step: str, run_url: str = ""):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        return

    text = f":warning: *IT 카드뉴스 생성 실패 — {date_str}*\n실패 단계: `{step}`"
    if run_url:
        text += f"\n<{run_url}|Actions 로그 보기>"

    payload = {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}
    requests.post(webhook_url, json=payload)
