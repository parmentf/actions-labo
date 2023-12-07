#!/usr/bin/env bash

set -euo pipefail


# branch name should be in the format:
# services/<service-name>/<comment>
BRANCH_NAME=$1
SERVICE_INTERMEDIATE=${BRANCH_NAME#services/} # remove services/ part
SERVICE_NAME=${SERVICE_INTERMEDIATE%/*} # remove comment part

if [ ! -d "services/$SERVICE_NAME" ]; then
    echo "Could not find directory services/$SERVICE_NAME"
    exit 1
fi

VERSION=$(node -e "console.log(require('./services/$SERVICE_NAME/package.json').version)")
TAG=ws-$SERVICE_NAME@$VERSION

echo "Building $TAG"

cd "services/$SERVICE_NAME"
npm run build
npm run publish
