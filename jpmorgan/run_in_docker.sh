#!/bin/bash

set -e

PROJECT_DIR=$(dirname "$0")
cd $PROJECT_DIR

docker build . -t python3.7

printf '\n\n'

docker run -v `pwd`:/host python3.7 python3 main.py $@
