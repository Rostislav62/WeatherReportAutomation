import schedule
import time
from datetime import datetime


def schedule_report(generate_report_func, daily_time="09:00"):
    """Schedule daily report generation."""
    schedule.every().day.at(daily_time).do(generate_report_func)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def run_once(generate_report_func):
    """Run report generation once."""
    generate_report_func()