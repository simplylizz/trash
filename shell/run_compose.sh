#!/bin/sh
#
# Run docker-compose in a container
#
# This script will attempt to mirror the host paths by using volumes for the
# following paths:
#   * $(pwd)
#   * $(dirname $COMPOSE_FILE) if it's set
#   * $HOME if it's set
#
# You can add additional volumes (or any docker run options) using
# the $COMPOSE_OPTIONS environment variable.
#


set -e

VERSION="1.29.1"
IMAGE="docker/compose:$VERSION"

ENV_TYPE="${ENV_TYPE:-dev}"

if [ $ENV_TYPE = "dev" ]; then
    COMPOSE_FILE="docker-compose.yml"
elif [ $ENV_TYPE = "prd" ]; then
    COMPOSE_FILE="docker-compose.prd.yml"
else
    echo "Unknown ENV_TYPE=$ENV_TYPE"
    exit 1
fi


# Setup options for connecting to docker host
if [ -z "$DOCKER_HOST" ]; then
    DOCKER_HOST="/var/run/docker.sock"
fi
if [ -S "$DOCKER_HOST" ]; then
    DOCKER_ADDR="-v $DOCKER_HOST:$DOCKER_HOST -e DOCKER_HOST"
else
    DOCKER_ADDR="-e DOCKER_HOST -e DOCKER_TLS_VERIFY -e DOCKER_CERT_PATH"
fi


# Setup volume mounts for compose config and context
if [ "$(pwd)" != '/' ]; then
    VOLUMES="-v $(pwd):$(pwd)"
fi
if [ -n "$COMPOSE_FILE" ]; then
    COMPOSE_OPTIONS="$COMPOSE_OPTIONS -e COMPOSE_FILE=$COMPOSE_FILE"
fi
#if [ -n "$HOME/.docker/config.json" ]; then
#    VOLUMES="$VOLUMES -v $HOME/.docker/config.json:/root/.docker/config.json"
#fi

# Only allocate tty if we detect one
if [ -t 0 -a -t 1 ]; then
    DOCKER_RUN_OPTIONS="$DOCKER_RUN_OPTIONS -t"
fi

# Always set -i to support piped and terminal input in run/exec
DOCKER_RUN_OPTIONS="$DOCKER_RUN_OPTIONS -i"


# Handle userns security
if [ ! -z "$(docker info 2>/dev/null | grep userns)" ]; then
    DOCKER_RUN_OPTIONS="$DOCKER_RUN_OPTIONS --userns=host"
fi

exec docker run --rm $DOCKER_RUN_OPTIONS $DOCKER_ADDR $COMPOSE_OPTIONS $VOLUMES -w "$(pwd)" $IMAGE "$@"
