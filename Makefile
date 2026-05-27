.PHONY: up down logs import test format

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

import:
	curl -X POST http://localhost:8000/data/import

test:
	pytest -q
