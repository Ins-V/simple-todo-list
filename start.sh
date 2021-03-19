#!/usr/bin/env bash

if [ -f backend/.env ]
then
  # shellcheck disable=SC2046
  # shellcheck disable=SC2002
  export $(cat backend/.env | sed 's/#.*//g' | xargs)
fi

# shellcheck disable=SC2086
uvicorn main:app --host=$SERVER_HOST --port=$SERVER_PORT --app-dir=./backend --reload
