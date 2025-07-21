# Use Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for curl (needed for health check)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY beacon_analyzer_app.py .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["python", "-m", "streamlit", "run", "beacon_analyzer_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
