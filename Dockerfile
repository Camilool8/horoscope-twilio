FROM python:3.12.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    flask==3.0.2 \
    requests==2.31.0

# Copy application code
COPY horoscope_sender.py .
COPY healthcheck.py .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check using curl (more reliable in containers)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port for health checks
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC
ENV HEALTH_PORT=8080

# Run the application
CMD ["python", "horoscope_sender.py"]