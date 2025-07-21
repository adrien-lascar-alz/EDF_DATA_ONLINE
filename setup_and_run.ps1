# Install required packages
Write-Host "Installing required packages..." -ForegroundColor Green
python -m pip install streamlit plotly matplotlib pandas

Write-Host ""
Write-Host "Starting Beacon Analyzer App..." -ForegroundColor Green
Write-Host "The app will open in your default browser at http://localhost:8501" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server when you're done." -ForegroundColor Yellow
Write-Host ""

# Run the Streamlit app using python -m to avoid PATH issues
python -m streamlit run beacon_analyzer_app.py
