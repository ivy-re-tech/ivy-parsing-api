#!/bin/bash

if [ -z "$1" ]; then
  echo "version not supplied"
  exit 1
fi
export VERSION=$1
FIMAGE=us.gcr.io/ivy-re-data/ivy-parser:"$VERSION"
echo "Building $FIMAGE..."
docker build -f compose/Dockerfile . --tag "$FIMAGE"
docker push "$FIMAGE"
