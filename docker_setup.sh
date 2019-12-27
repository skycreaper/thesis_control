#!/bin/sh
if [ -d "docker-compose" ]; then
    echo "docker-compose wasn't found"
else
    echo "Creating .env file..."
    echo "PYTHON_PORT=8090
POSTGRES_HOST=postgres
POSTGRES_DB=thesis_control
POSTGRES_USER=thesis_dev
POSTGRES_PASSWORD=
DB_PORT=5433" > .env
    echo "creating network 'thesis_control_network'"
    docker network create thesis_control_network
    echo "raising up containers..."
    docker-compose up
fi