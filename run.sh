#!/bin/sh

PORT="${PORT:-8080}"

uvicorn \
    --factory src:create_app \
    --port $PORT \
    --host 0.0.0.0 \
    --proxy-headers \
    --reload \
    --reload-dir ./src
