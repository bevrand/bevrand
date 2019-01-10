#!/usr/bin/env bash

set -ex

docker build -t dockerswagger .

old_id=$(docker ps | grep :4530 | awk {'print$1'})
echo "${old_id}"

if [  -n "$old_id" ]; then
    docker rm -f "$old_id"
fi

#docker rmi $(docker images | grep none | awk '{print$3}')

docker run -d -p 4530:8080 --name dockerswagger dockerswagger
