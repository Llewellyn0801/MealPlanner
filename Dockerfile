FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "uvicorn", "meal_planner.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
