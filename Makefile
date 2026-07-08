.PHONY: up down test migrate

up:
	docker compose up

down:
	docker compose down

test:
	docker compose exec web pytest

migrate:
	docker compose exec web python manage.py makemigrations
	docker compose exec web python manage.py migrate