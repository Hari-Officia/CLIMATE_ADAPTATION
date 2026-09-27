"""
Quarterly Review Scheduler
Manages quarterly and annual review schedules from config/governance/quarterly_review_schedule.json.
"""
import json
from pathlib import Path

SCHEDULE_FILE = Path("config/governance/quarterly_review_schedule.json")

def get_schedule():
    if not SCHEDULE_FILE.exists():
        return {
            "next_quarterly_review": "2026-12-23",
            "annual_recertification": "2027-09-23",
            "certification_expiry": "2027-09-23"
        }
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("schedule", {})
