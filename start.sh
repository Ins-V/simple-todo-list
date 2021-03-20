#!/usr/bin/env bash

if [ -f .env ]
then
  # shellcheck disable=SC2046
  # shellcheck disable=SC2002
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# shellcheck disable=SC2086
uvicorn main:app --host=$SERVER_HOST --port=$SERVER_PORT --app-dir=./src --reload
