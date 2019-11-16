#!/bin/bash

if [ -z "$1" ]; then
  echo "version not supplied"
  exit 1
fi

deploy/build.sh "$1"
deploy/deploy.sh "$1"
