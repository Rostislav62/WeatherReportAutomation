import pandas as pd
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Google Sheets configuration
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS")


def create_excel_report(weather_data, output_file):
    """Create a formatted Excel report."""
    if not weather_data:
        print("No weather data provided. Skipping Excel report creation.")
        return

    df = pd.DataFrame(weather_data)

    # Create workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Weather Report"

    # Add title
    ws.merge_cells("A1:E1")
    ws["A1"] = f"Weather Report - {datetime.now().strftime('%Y-%m-%d')}"
    ws["A1"].font = Font(size=16, bold=True)
    ws["A1"].alignment = Alignment(horizontal="center")

    # Add headers
    headers = ["City", "Date", "Temperature (°C)", "Precipitation (mm)", "Humidity (%)"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col)
        cell.value = header
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")
        cell.border = Border(left=Side(style="thin"),
                             right=Side(style="thin"),
                             top=Side(style="thin"),
                             bottom=Side(style="thin"))

    # Add data
    for row, data in enumerate(weather_data, 4):
        ws.cell(row=row, column=1).value = data["city"]
        ws.cell(row=row, column=2).value = data["date"]
        ws.cell(row=row, column=3).value = data["temperature"]
        ws.cell(row=row, column=4).value = data["precipitation"]
        ws.cell(row=row, column=5).value = data["humidity"]

        # Add borders to data cells
        for col in range(1, 6):
            ws.cell(row=row, column=col).border = Border(left=Side(style="thin"),
                                                         right=Side(style="thin"),
                                                         top=Side(style="thin"),
                                                         bottom=Side(style="thin"))

    # Create chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["city"], df["temperature"], color="skyblue")
    plt.title("Temperature by City")
    plt.xlabel("City")
    plt.ylabel("Temperature (°C)")
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.savefig("temp_chart.png")
    plt.close()

    # Add chart to Excel
    img = openpyxl.drawing.image.Image("temp_chart.png")
    ws.add_image(img, "A10")

    # Adjust column widths (avoid merged cells)
    column_widths = {"A": 15, "B": 20, "C": 15, "D": 15, "E": 15}  # Predefined widths
    for col_letter, width in column_widths.items():
        ws.column_dimensions[col_letter].width = width

    # Save the workbook
    wb.save(output_file)
    print(f"Excel report saved as {output_file}")


def create_gsheets_report(weather_data, spreadsheet_name="Weather Reports"):
    """Create a formatted Google Sheets report."""
    if not weather_data:
        print("No weather data provided. Skipping Google Sheets report creation.")
        return

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        spreadsheet = client.create(spreadsheet_name)
        spreadsheet.share(os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"), perm_type="user", role="writer")

    worksheet = spreadsheet.sheet1

    # Clear existing content
    worksheet.clear()

    # Add title
    title = f"Weather Report - {datetime.now().strftime('%Y-%m-%d')}"
    worksheet.update("A1:E1", [[title]])  # Use list of lists for single cell
    worksheet.format("A1:E1", {
        "textFormat": {"fontSize": 16, "bold": True},
        "horizontalAlignment": "CENTER"
    })
    worksheet.merge_cells("A1:E1")

    # Add headers
    headers = ["City", "Date", "Temperature (°C)", "Precipitation (mm)", "Humidity (%)"]
    worksheet.update("A3:E3", [headers])  # Headers as a single row
    worksheet.format("A3:E3", {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.68, "green": 0.85, "blue": 0.90},
        "horizontalAlignment": "CENTER",
        "borders": {
            "top": {"style": "SOLID"},
            "bottom": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "right": {"style": "SOLID"}
        }
    })

    # Add data
    data_rows = [[d["city"], d["date"], d["temperature"], d["precipitation"], d["humidity"]]
                 for d in weather_data]
    worksheet.update("A4:E" + str(4 + len(data_rows) - 1), data_rows)

    # Add borders to data
    worksheet.format(f"A4:E{4 + len(data_rows) - 1}", {
        "borders": {
            "top": {"style": "SOLID"},
            "bottom": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "right": {"style": "SOLID"}
        }
    })

    print(f"Google Sheets report updated: {spreadsheet_name}")