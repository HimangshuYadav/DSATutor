# High-Performance DSATutor Environment
# Optimized for Hugging Face Spaces and OpenEnv Compliance

FROM python:3.12-slim

# System dependencies for safety and performance
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependency layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application layer
COPY . .

# Environment defaults
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Expose API port
EXPOSE 7860

# Fast startup
CMD ["python", "-m", "server.app"]
