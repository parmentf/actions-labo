#!/usr/bin/env bash

set -euo pipefail

# Branch name should be in the format:
# <service>/<major|minor|patch>/<comment>
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
SERVICE_NAME=${BRANCH_NAME%%/*}
VERSION_INTERMEDIATE=${BRANCH_NAME#*/}
VERSION_TYPE=${VERSION_INTERMEDIATE%/*} # major, minor or patch

echo "Building $VERSION_TYPE version of $SERVICE_NAME"

if [ -d "services/$SERVICE_NAME" ]; then
    cd "services/$SERVICE_NAME"
    npm version "$VERSION_TYPE"
else
    echo "Could not find service $SERVICE_NAME"
    exit 1
fi
