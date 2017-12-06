#!/usr/bin/env sh


echo $(docker-compose build)

DOCKERIMAGES=$(docker images | grep bevrand_  | awk '{ print $1} ' )

for image in $DOCKERIMAGES; do
    PUSHIMAGE=bevrand/$image
    echo $PUSHIMAGE
    if [ "$image" == 'bevrand_mongoapi' ]
    then
        $(docker tag $image bevrand/$image)
	echo $(docker push $PUSHIMAGE)
    elif [ "$image" == 'bevrand_randomizerapi' ]
    then    
        $(docker tag $image bevrand/$image)
	echo $(docker push $PUSHIMAGE)
    elif [ "$image" == 'bevrand_nodefrontend' ]
    then
        $(docker tag $image bevrand/$image)
	echo $(docker push $PUSHIMAGE)
     elif [ "$image" == 'bevrand_mongoseeder' ]
     then	
	 $(docker tag $image bevrand/$image)
         echo $(docker push $PUSHIMAGE)
    fi
done



