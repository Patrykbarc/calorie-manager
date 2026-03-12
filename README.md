# Calories Counter

A calorie tracking application with a REST API and a CLI interface.

## Requirements

- Python 3.11+
- pip or uv
- Docker & Docker Compose

## Running Locally

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 2. Install dependencies

```bash
pip install -e ".[dev]"
```

### 3. Start the API server

```bash
make server
```

The API will be available at `http://localhost:8000`.

Alternatively, run directly:

```bash
fastapi dev app/api/api.py
```

### 4. Run the CLI

```bash
make cli
```

Or directly:

```bash
python3 main.py
```

## Running with Docker

### Start the API server

```bash
docker compose up
```

The API will be available at `http://localhost:8000`.

To rebuild the image after code changes:

```bash
docker compose up --build
```

## API Endpoints

| Method | Endpoint                  | Description                  |
|--------|---------------------------|------------------------------|
| GET    | `/healthz`                | Health check                 |
| GET    | `/meals`                  | Get all meals                |
| POST   | `/meals`                  | Add a new meal               |
| GET    | `/meals/total-nutritions` | Get total nutrition summary  |
| PUT    | `/meals/{id}`             | Update a meal by ID          |
| DELETE | `/meals/{id}`             | Delete a meal by ID          |

Interactive API docs (Swagger UI) are available at `http://localhost:8000/docs`.

## Running Tests

```bash
pytest
```
