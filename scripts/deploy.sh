#!/bin/bash

clear
source ./scripts/env.sh
source ./scripts/build.sh

clear

docker build -t gitmr-app src/.

if docker container inspect gitmr-app &> /dev/null; then
    echo "Removing existing gitmr-app container..."
    docker container rm -f gitmr-app
fi

docker run -d --name gitmr-app -p 8080:8080 gitmr-app

echo "gitmr-app container is up and running on http://localhost:8080"
open http://localhost:8080
