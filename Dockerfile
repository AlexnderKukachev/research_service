FROM python:3.11-slim AS base

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Test stage
FROM base AS test
RUN pip install pytest anyio httpx aiosqlite
ENV PYTHONPATH=/app
CMD ["pytest", "tests"]
