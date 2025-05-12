import argparse
from api import get_all_weather_data
from report import create_excel_report, create_gsheets_report
from scheduler import schedule_report, run_once
from datetime import datetime


def generate_report():
    """Generate weather reports for both Excel and Google Sheets."""
    print(f"Generating report at {datetime.now()}")

    # Get weather data
    weather_data = get_all_weather_data()

    if not weather_data:
        print("No weather data retrieved. Aborting report generation.")
        return

    # Generate reports
    excel_file = f"weather_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    create_excel_report(weather_data, excel_file)
    create_gsheets_report(weather_data)

    print(f"Reports generated successfully: {excel_file} and Google Sheet")


def main():
    parser = argparse.ArgumentParser(description="Weather Report Automation")
    parser.add_argument("--once", action="store_true",
                        help="Run report generation once and exit")
    args = parser.parse_args()

    if args.once:
        run_once(generate_report)
    else:
        print("Starting scheduled report generation (test at 16:32)")
        schedule_report(generate_report, daily_time="16:32")  # Temporary test time


if __name__ == "__main__":
    main()