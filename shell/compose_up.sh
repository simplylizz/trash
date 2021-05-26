#!/bin/sh

set -e

./run_compose.sh docker-compose up --no-build $@
