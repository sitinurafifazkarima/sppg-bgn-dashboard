FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY dashboard_sppg.py .
COPY sppg_data_complete_with_coordinates.csv .
COPY README.md .
COPY METODOLOGI.md .

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

# Run the application
CMD ["streamlit", "run", "dashboard_sppg.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]
