# WeatherReportAutomation: Automated Weather Report Generator

## Overview

### Problem
Office workers and analysts often need to compile weather data for reports, but manually collecting and formatting this data from APIs into Excel or Google Sheets is time-consuming and prone to errors.

### Solution
WeatherReportAutomation is a Python-based tool that automates the collection of weather data from the OpenWeatherMap API and generates formatted reports in both Excel and Google Sheets. It supports manual and scheduled report generation, saving time and ensuring consistent, professional outputs.

### Impact
Streamlines data collection and report creation for businesses, analysts, and researchers, enabling faster decision-making with accurate and visually appealing weather reports.

## About the Project
WeatherReportAutomation is a Python script designed to fetch current weather data for specified cities (Moscow, London, New York) and produce formatted reports in Excel and Google Sheets. It uses the OpenWeatherMap API for data retrieval, `pandas` and `openpyxl` for Excel reports, `gspread` for Google Sheets integration, and `schedule` for automation. The project demonstrates my skills in API integration, data processing, automation, and report generation.

## Features
- **Weather Data Collection**: Fetches temperature, precipitation, and humidity for multiple cities via OpenWeatherMap API.
- **Excel Reports**: Generates formatted `.xlsx` files with tables, headers, and a temperature bar chart.
- **Google Sheets Reports**: Updates a Google Sheet with formatted tables and headers.
- **Scheduled Automation**: Supports daily report generation (e.g., at 9:00) using the `schedule` library.
- **Manual Execution**: Allows one-time report generation via command-line argument.
- **Secure Configuration**: Stores API keys and credentials in a `.env` file.

## How to Work with WeatherReportAutomation

### Access the Tool
Run the script locally by following the Setup Instructions below. No external bot or service is required.

### User Workflow
1. **Configure the Environment**:
   - Set up API keys and Google Sheets credentials in `.env`.
2. **Run Manually**:
   - Execute `python src/main.py --once` to generate reports immediately.
3. **Run on Schedule**:
   - Execute `python src/main.py` to start daily report generation (default: 9:00).
4. **Check Outputs**:
   - Excel report saved in the project root (e.g., `weather_report_20250512_163259.xlsx`).
   - Google Sheet (`Weather Reports`) updated with the latest data.

### Example Usage
- Run manually:
  ```bash
  python src/main.py --once
  ```
  Output:
  ```
  Generating report at 2025-05-12 16:32:58
  Excel report saved as weather_report_20250512_163259.xlsx
  Google Sheets report updated: Weather Reports
  Reports generated successfully: weather_report_20250512_163259.xlsx and Google Sheet
  ```
- Run on schedule:
  ```bash
  python src/main.py
  ```
  Output (at 9:00 daily):
  ```
  Starting scheduled report generation (daily at 09:00)
  Generating report at 2025-05-13 09:00:00
  Excel report saved as weather_report_20250513_090000.xlsx
  Google Sheets report updated: Weather Reports
  Reports generated successfully: weather_report_20250513_090000.xlsx and Google Sheet
  ```

### Notes
- The script collects current weather data for Moscow, London, and New York. Modify `api.py` to change cities.
- Excel reports include a bar chart; Google Sheets reports are table-only for simplicity.
- Ensure API keys and Google Sheets credentials are configured correctly in `.env`.

## Setup Instructions

### Create Virtual Environment
1. Create a project directory:
   ```bash
   mkdir WeatherReportAutomation
   cd WeatherReportAutomation
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/macOS
   ```
3. Install dependencies:
   ```bash
   pip install requests pandas openpyxl xlsxwriter gspread google-auth python-dotenv matplotlib schedule
   pip freeze > requirements.txt
   ```

### Configure API Keys and Google Sheets
1. Create a `.env` file in the project root:
   ```
   OPENWEATHER_API_KEY=your_openweathermap_api_key_here
   GOOGLE_SHEETS_CREDENTIALS=credentials.json
   GOOGLE_SHEETS_CLIENT_EMAIL=your_service_account_email_here
   ```
   - **OpenWeatherMap API Key**:
     - Register at [openweathermap.org](https://openweathermap.org/).
     - Copy the API key from your profile.
   - **Google Sheets Credentials**:
     - Create a Service Account in [Google Cloud Console](https://console.cloud.google.com/).
     - Enable Google Sheets API and Google Drive API.
     - Download the JSON key file as `credentials.json` and place it in the project root.
     - Share the Google Sheet (`Weather Reports`) with the Service Account email (`client_email` from `credentials.json`) with `Editor` access.

### Project Structure
1. Create the following structure:
   ```
   WeatherReportAutomation/
   ├── src/
   │   ├── main.py           # Main script for manual and scheduled execution
   │   ├── api.py            # Weather data retrieval from OpenWeatherMap
   │   ├── report.py         # Report generation for Excel and Google Sheets
   │   ├── scheduler.py      # Scheduling logic for automation
   ├── .env                  # API keys and credentials
   ├── credentials.json      # Google Service Account credentials
   ├── requirements.txt      # Dependencies
   ├── README.md             # Project documentation
   ```

### Run the Script
1. Start the script:
   - For one-time execution:
     ```bash
     python src/main.py --once
     ```
   - For scheduled execution:
     ```bash
     python src/main.py
     ```

## API Keys
The tool uses external services:
- **OpenWeatherMap API**: Obtain a free API key from [openweathermap.org](https://openweathermap.org/).
- **Google Sheets API**: Configure a Service Account in [Google Cloud Console](https://console.cloud.google.com/) with access to Google Sheets and Drive APIs.

## Project Structure
- `src/main.py` — Entry point for manual and scheduled report generation.
- `src/api.py` — Logic for fetching weather data from OpenWeatherMap API.
- `src/report.py` — Report creation for Excel and Google Sheets with formatting and charts.
- `src/scheduler.py` — Automation logic for daily report scheduling.
- `.env` — Environment variables for API keys and credentials.
- `requirements.txt` — List of Python dependencies.

## Technologies
- **Python 3.12.4**: Core language.
- **requests**: HTTP requests for API calls.
- **pandas**: Data processing and manipulation.
- **openpyxl/xlsxwriter**: Excel report generation.
- **gspread/google-auth**: Google Sheets integration.
- **matplotlib**: Chart creation for Excel reports.
- **schedule**: Task scheduling for automation.
- **python-dotenv**: Environment variable management.
- **Git**: Version control (to be initialized).

## Author
Rostislav — Python developer specializing in automation, API integration, and data processing. This project is part of my portfolio, showcasing expertise in data automation, report generation, and API-driven solutions.

## License
MIT License