#!/bin/bash

set -e

source ./venv/bin/activate

cd string_counter

pytest ${@:-.}
