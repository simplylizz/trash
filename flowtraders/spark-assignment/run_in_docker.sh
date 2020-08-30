#!/bin/bash

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $PROJECT_DIR

mount_project="--mount type=bind,source=${PROJECT_DIR},destination=/project"

if [ -d "${HOME}/.ipython" ]; then
    mount_ipython="--mount type=bind,source=${HOME}/.ipython,destination=/root/.ipython"
else
    mount_ipython=""
fi

docker_image_name="pyspark-clean"

if [ "${NO_BUILD}" != "1" ]; then
    docker build -t $docker_image_name .
fi

docker run \
    -it \
    $mount_project \
    $mount_ipython \
    -w="/project" \
    --rm \
    --name $docker_image_name \
    $docker_image_name:latest \
    ${@:pytest --doctest-modules}
