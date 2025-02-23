run:
	docker compose run --rm app

auto:
	docker compose run --rm app python main.py -a

build:
	docker compose build