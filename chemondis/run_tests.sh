#!/bin/bash

set -e

PROJECT_DIR=$(dirname "$0")
cd $PROJECT_DIR

docker build . -t chemondis
docker run -it chemondis test
