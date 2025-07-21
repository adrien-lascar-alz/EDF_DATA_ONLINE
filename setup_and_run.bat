@echo off
echo Installing required packages...
python -m pip install streamlit plotly matplotlib pandas

echo.
echo Starting Beacon Analyzer App...
echo The app will open in your default browser at http://localhost:8501
echo Press Ctrl+C to stop the server when you're done.
echo.

REM Use python -m streamlit instead of just streamlit to avoid PATH issues
python -m streamlit run beacon_analyzer_app.py

pause
