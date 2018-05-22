#!/usr/bin/env sh

DOCKERIMAGES=$(docker images | grep bevrand_  | awk '{ print $1} ' )

for image in $DOCKERIMAGES; do
    PUSH_IMAGE="${image#*_}"
    PUSH_IMAGE="bevrand/$PUSH_IMAGE"
    echo $PUSH_IMAGE
    $(docker tag $image $PUSH_IMAGE:latest)
    echo $(docker push $PUSH_IMAGE:latest)
done





