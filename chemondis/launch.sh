#!/bin/bash

set -e

PROJECT_DIR=$(dirname "$0")
cd $PROJECT_DIR

docker build . -t chemondis

docker stop chemondis >/dev/null || true
docker rm chemondis >/dev/null || true

docker run -v `pwd`/chemondis:/app -p 8080:8080 --name chemondis chemondis
