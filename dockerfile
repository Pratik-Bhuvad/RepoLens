# ── Base image ──────────────────────────────────────────────
FROM python:3.10-slim

# ── Metadata (good practice) ────────────────────────────────
LABEL maintainer="yourname@email.com"
LABEL version="1.0"

# ── Security: don't run as root ─────────────────────────────
RUN useradd --create-home appuser

# ── Working directory ───────────────────────────────────────
WORKDIR /app

# ── Install dependencies ────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy source code ────────────────────────────────────────
COPY . .

# ── Switch to non-root user ─────────────────────────────────
USER appuser

# ── Entry point ─────────────────────────────────────────────
# Default args (can be overridden at runtime)
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]