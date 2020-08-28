#!/bin/bash

# Runs the app, eq. make dev
FLASK_APP=redisolar flask load
FLASK_ENV=development FLASK_APP=redisolar FLASK_DEBUG=1 flask run --port=8081 --host=0.0.0.0
