"""
GitHub Actions 워크플로우 실패 시 Slack 에러 알림.
환경변수: SLACK_WEBHOOK_URL, GH_REPO, GITHUB_RUN_ID
"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from slack_notify import send_error

today = datetime.utcnow().strftime("%Y-%m-%d")
repo = os.environ.get("GH_REPO", "")
run_id = os.environ.get("GITHUB_RUN_ID", "")
run_url = f"https://github.com/{repo}/actions/runs/{run_id}" if repo and run_id else ""

send_error(today, step="파이프라인", run_url=run_url)
