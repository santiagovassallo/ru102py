# RediSolar Python

This is the sample application codebase for the Redis University course [RU102PY, Redis for Python Developers](https://university.redislabs.com/courses/ru102py/).

## Setup

Please note, this is my twist to the original code, since I wanted to be able to follow along the course using PyCharm
and my local docker. As I currently using Ubuntu 18.04, with these aproach it doesn't matter that my SO has python 3.6,
and I don't have to install other applications. Docker will take care of them.

### Prerequisites

To start and run this application, you will need `docker` and `docker-compose`

### Setting up Python dependencies with make

This project automates setting up its Python dependencies with `make`.

But you don't have to worry about this, because docker will make it for you.

#### Virtualenv

As the project run inside a container, we don't need a virtual env, so it doesn't exist here.

### Redis and RedisTimeSeries

This project requires a connection to Redis and uses the RedisTimeSeries module, but once again, docker-compose will
care about that.

#### Key prefixes

This project prefixes all keys with a string. By default, the dev server and
sample data loader use the prefix "ru102py-app:", while the test suite uses
"ru102py-test:".

When you run the tests, they add keys to the same Redis database that the
running Flask application uses, but with the prefix "test:". Then when the
tests finish, the test runner deletes all the keys prefixed with "test:".

You can change the prefix used for keys by changing the `REDIS_KEY_PREFIX`
option in the following files:

- `redisolar/instance/dev.cfg`
- `redisolar/instance/testing.cfg`

## Running the project

To run the project you just need to run docker-compose like this

`docker-compose run --rm --service-ports test bash`

This will open a terminal for you, where you can run all the following commands. Please note, as docker-compose will
share the source code of the project through a volume, every change you make in the source files from your machine will
be seen in the container.

There is a convenience file in the project called `run.sh`. Just by doing `source run.sh` you can spin up the project.

### Loading sample data

Before the example app will do anything interesting, it needs data.

You can use the command `make load` to load solar sites and generate example
readings. `make load` loads data into the Redis instance that you configured in
`redisolar/instance/dev.cfg`, using the `REDIS_HOST` and `REDIS_PORT` defined there.

**Note**: Since the database doesn't persist when you stop the project, you'll need to run this command everytime you
spin up the project.

### Running the dev server

Run the development server with `make dev`.

**Note:** By default, the server runs with geographic features disabled. To run
with geo features enabled, set the option `USE_GEO_SITE_API` in
`redisolar/instance/dev.cfg` to `True`.

After running `make dev` access https://localhost:8081 to see the app.

**Don't see any data?**
The first time you run `make dev`, you may see a map with nothing on it. In
order to see sites on the map, you'll need to do two things:

1. Follow the instructions in this README to load data
2. Complete Challenge #1 in the course

#### Running the dev server manually

If you need to override command-line flags when running Flask, you can use the `flask` command to run the dev server manually.

To run the `flask` command:

    $ FLASK_APP=redisolar flask run --port=8081

### Running tests

You can run `make test` to run the unit tests.

#### Running tests manually

You can run individual tests by calling `pytest` manually. To do, run `pytest` with whatever options you want.

For example, here is how you run a specific test:

    $ pytest -k test_set_get

## Questions?

Chat with our teaching assistants on the [Redis University Discord Server](https://discord.gg/k5wr43E).

## License

This project is released under the MIT license. See LICENSE for the full text.
