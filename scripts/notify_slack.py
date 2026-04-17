"""
GitHub Actions 워크플로우에서 git push 후 실행되는 Slack 알림 스크립트.
환경변수: SLACK_WEBHOOK_URL, GH_REPO
"""
import glob
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from slack_notify import send_daily_card

today = datetime.utcnow().strftime("%Y-%m-%d")
repo = os.environ.get("GH_REPO", "")
user = repo.split("/")[0] if "/" in repo else ""
name = repo.split("/")[1] if "/" in repo else "it-news"

page_url = f"https://{user}.github.io/{name}/{today}.html"
thumbnail_url = f"https://{user}.github.io/{name}/{today}/card_01.png"

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
card_count = len(glob.glob(os.path.join(root, "docs", today, "card_*.png")))

send_daily_card(today, page_url, card_count=card_count, thumbnail_url=thumbnail_url)
