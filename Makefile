PYTHON = python3
API_PATH = app/api/api.py

server:
	fastapi dev ${API_PATH}

start:
	python3 main.py
