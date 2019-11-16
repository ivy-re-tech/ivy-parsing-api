#!/bin/bash

if [ -z "$1" ]; then
  echo "version not supplied"
  exit 1
fi
export VERSION=$1

envsubst < deploy/IvyParser.yml | kubectl apply -f -
