#!/usr/bin/env bash

success=false

for i in {1..30}; do
    echo "Checking if services are available. Attempt: ${i}"

    #proxyapi
    wget -O /dev/null localhost:4540/playlist-api/v2/frontpage && \
    #playlistapi
    wget -O /dev/null localhost:4550/api/v1/public && \
    #randomizerapi
    wget -O /dev/null localhost:4560/api/ping && \
    #authenticationapi
    wget -O /dev/null localhost:4570/api/Users && \
    #highscoreapi
    wget -O /dev/null localhost:4580/ping && \
    #recommendationapi
    wget -O /dev/null localhost:4590/ping && \

	success=true && break || sleep 2; done

if [[ $success = false ]] ; then
    echo "After 30 tries services are still unavailable"
    exit 1
fi

echo "Services up and ready to go!"