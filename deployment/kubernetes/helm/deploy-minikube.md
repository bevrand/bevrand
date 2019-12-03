Minikube:

minikube start --profile bevrand --kubernetes-version=v1.11.10 --memory=6144 --cpus=4
minikube --profile fbs addons enable ingress
eval $(minikube -p bevrand docker-env)
minikube -p bevrand start 
minikube -p bevrand stop


hosts:

# voor minikube
192.168.99.100	bevrand

Dit ip komt uit:

minikube -p bevrand ip


