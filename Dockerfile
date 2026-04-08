# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Copy only requirements to leverage cache
COPY requirements.txt .

# Install dependencies into a specific directory
RUN pip install --no-cache-dir --prefix=/build/local -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set up a new user with UID 1000 for HF Spaces
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=/home/user/app

WORKDIR $HOME/app

# Copy installed dependencies from builder
COPY --from=builder --chown=user /build/local /home/user/.local

# Copy source code (respects .dockerignore)
COPY --chown=user . .

# Environment Variables
ENV API_BASE_URL=http://0.0.0.0:7860
ENV MODEL_NAME=llama-3.3-70b-versatile
ENV PORT=7860

# Expose mandatory HF Space port
EXPOSE 7860

# CMD to run the server
CMD ["python3", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
