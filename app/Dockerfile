# Build stage
FROM python:3.10 as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional libhdf5-dev libnetcdf-dev libudunits2-dev gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt /
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt

# Application stage
FROM python:3.10-slim

# Copy virtual environment from the builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /root/.cache /root/.cache

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set working directory
WORKDIR /app

# Copy application code and entrypoint script
COPY . /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Clean up unnecessary files
RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional \
    && rm -rf /var/lib/apt/lists/* \
    && pip cache purge

# Expose the application port
EXPOSE 5000

# Set entrypoint and default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
