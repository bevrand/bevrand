#!/bin/bash

echo "starting"
$(docker tag bevrand_nodefrontend bevrand/reactfrontend:develop)
echo "pushing"
echo $(docker push bevrand/reactfrontend:develop)
echo "Done pushing"