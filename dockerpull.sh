#!/bin/bash

echo $(docker pull bevrand/bevrand_nodefrontend)
echo $(docker pull bevrand/bevrand_randomizerapi)
echo $(docker pull bevrand/bevrand_mongoapi)
echo $(docker pull bevrand/bevrand_mongoseeder)


$(docker tag bevrand/bevrand_nodefrontend bevrand_nodefrontend)
$(docker tag bevrand/bevrand_randomizerapi bevrand_randomizerapi)
$(docker tag bevrand/bevrand_mongoapi bevrand_mongoapi)
$(docker tag bevrand/bevrand_mongoseeder bevrand_mongoseeder)


DOCKERIMAGES=$(docker images | grep bevrand_  | awk '{ print $1} ' )

echo $DOCKERIMAGES

$DELETED=$(docker rmi $(docker images --filter "dangling=true" -q --no-trunc))
echo $DELETED
