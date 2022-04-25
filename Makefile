makemigrations:
	docker exec -w /src -it shop_authentication_1 alembic revision --autogenerate -m "$(name)"

migrate:
	docker exec -w /src -it shop_authentication_1 alembic upgrade head