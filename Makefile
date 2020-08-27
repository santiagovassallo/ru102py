APP := redisolar
PORT := 8081

ifeq (${IS_CI}, true)
	FLAGS := "--ci"
else
	FLAGS := "-s"
endif

.PHONY: mypy test all clean dev load frontend timeseries-docker

all: mypy lint test

env: requirements.txt
	pip install wheel; pip install -Ue ".[dev]"

mypy:
	mypy --ignore-missing-imports redisolar

test:
	pytest $(FLAGS)

lint:
	pylint redisolar

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

dev:
	FLASK_ENV=development FLASK_APP=$(APP) FLASK_DEBUG=1 flask run --port=$(PORT) --host=0.0.0.0

frontend:
	cd frontend; npm run build
	rm -rf redisolar/static
	cp -r frontend/dist/static redisolar/static
	cp frontend/dist/index.html redisolar/static/

load:
	FLASK_APP=$(APP) flask load
