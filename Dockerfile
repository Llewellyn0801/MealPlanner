FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
	CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)"

CMD ["sh", "-c", "uv run alembic upgrade head && uv run python -m uvicorn meal_planner.main:app --app-dir src --host 0.0.0.0 --port 8000"]
