import argparse
from api import get_all_weather_data
from report import create_excel_report, create_gsheets_report
from scheduler import schedule_report, run_once
from datetime import datetime


def generate_report(style="minimal"):
    """Generate weather reports for both Excel and Google Sheets."""
    print(f"Generating report at {datetime.now()} with style: {style}")

    # Get weather data
    weather_data = get_all_weather_data()

    if not weather_data:
        print("No weather data retrieved. Aborting report generation.")
        return

    # Generate reports
    excel_file = f"weather_report_{style}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    create_excel_report(weather_data, excel_file, style=style)
    create_gsheets_report(weather_data)

    print(f"Reports generated successfully: {excel_file} and Google Sheet")


def main():
    parser = argparse.ArgumentParser(description="Weather Report Automation")
    parser.add_argument("--once", action="store_true",
                        help="Run report generation once and exit")
    parser.add_argument("--style", choices=["minimal", "modern", "corporate"],
                        default="minimal", help="Excel report style")
    args = parser.parse_args()

    if args.once:
        run_once(lambda: generate_report(args.style))
    else:
        print("Starting scheduled report generation (daily at 09:00)")
        # Эту команду нужно запускать чтобы, получить ежедневный отчёт от 9 часов.
        # python src/main.py - -style corporate
        # Эту команду нужно запускать чтобы, получить одноразовый отчёт.
        # python src/main.py --once --style corporate
        schedule_report(lambda: generate_report(args.style), daily_time="09:00")


if __name__ == "__main__":
    main()