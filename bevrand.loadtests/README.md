Loadtests made in artillery

Local file is for local testing with docker-compose
DO testsuite does pretty much the same but in digital ocean, mostly for future purposes to see how 
k8s/docker swarm would hold up.

npm install -g artillery
artillery dino


artillery run hello.yml