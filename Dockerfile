# Multi-stage Dockerfile for running the app
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Needed for some packages (pandas, yfinance may need build deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . /app

EXPOSE 80

# Default command: run the ASGI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
