# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    Professional Video Downloader Bot                         ║
# ║                         Docker Configuration                                 ║
# ║                                                                              ║
# ║  Build:  docker build -t video-downloader-bot .                              ║
# ║  Run:    docker run -d --name vdbot --env-file .env video-downloader-bot     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 1: Base Image
# ═══════════════════════════════════════════════════════════════════════════════

FROM python:3.11-slim-bookworm AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 2: Builder
# ═══════════════════════════════════════════════════════════════════════════════

FROM base AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 3: Production
# ═══════════════════════════════════════════════════════════════════════════════

FROM base AS production

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN groupadd -r botuser && useradd -r -g botuser botuser

# Create required directories
RUN mkdir -p /app/temp /app/downloads /app/cookies /app/logs /app/cache /app/database \
    && chown -R botuser:botuser /app

# Copy application code
COPY --chown=botuser:botuser . .

# Switch to non-root user
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command
CMD ["python", "-u", "bot.py"]

# ═══════════════════════════════════════════════════════════════════════════════
# LABELS
# ═══════════════════════════════════════════════════════════════════════════════

LABEL maintainer="Video Downloader Team" \
      version="2.0.0" \
      description="Professional Video Downloader Telegram Bot" \
      org.opencontainers.image.source="https://github.com/your-repo/video-downloader-bot"