FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install -e ".[dev]"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.api.api:api", "--host", "0.0.0.0", "--port", "8000", "--reload"]
