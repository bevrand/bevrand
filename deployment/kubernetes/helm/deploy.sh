#!/usr/bin/env bash

set -e

OPS_DIR=$(cd "$( dirname -- "${BASH_SOURCE[0]}" )" && cd .. && pwd)

# Default to local with namesapce default
if [[ -z $ENV_TARGET ]]; then
    export ENV_DIR="$OPS_DIR/helm/env/minikube"
else
    export ENV_DIR="$OPS_DIR/helm/env/$ENV_TARGET"
fi
if [[ -z $NAMESPACE ]]; then
    export NAMESPACE='default'
fi

CHART_DIR="$OPS_DIR/helm/bevrand"
WORKDIR="$(cd "$ENV_DIR" && pwd)"

helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm upgrade --install rabbit --namespace "$NAMESPACE" --set rabbitmq.username=admin,rabbitmq.password=bevrand stable/rabbitmq
helm upgrade --install nginx-ingress --namespace "$NAMESPACE" --set controller.publishService.enabled=true stable/nginx-ingress

cd "$WORKDIR"
for name in $(find * -maxdepth 0 -type d | sort); do
    cd "$CHART_DIR/.."
    yaml_files="$(ls "$ENV_DIR/$name/" | grep yaml)"
    for file in $yaml_files; do
        cmd=(helm upgrade --install --namespace "$NAMESPACE" --values "$ENV_DIR/$name/$file")
        cmd+=($(echo $file | cut -d'.' -f1)) 
        cmd+=("$CHART_DIR/$name")
        echo "${cmd[@]}"
        "${cmd[@]}"
    done
done
