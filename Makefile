.PHONY: build up down logs test shell

build:
	docker-compose build

up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose run --rm app python -m pytest -q

shell:
	docker-compose run --rm app /bin/bash
