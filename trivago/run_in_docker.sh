#!/bin/bash

set -e

PROJECT_DIR=$(dirname "$0")
cd $PROJECT_DIR

docker build . -t trivago

docker run -v `pwd`:/host trivago python3 /host/trivago/main.py $@
