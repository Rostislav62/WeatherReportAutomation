@echo off
cd /d "C:\Users\rsmiglix\Documents\WeatherReportAutomation"
call venv\Scripts\activate
python src\main.py --style corporate
deactivate