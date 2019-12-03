#!/usr/bin/env sh

if which doctl > /dev/null; then
    echo "doctl installed good to go"
else
  curl -sL https://github.com/digitalocean/doctl/releases/download/v1.35.0/doctl-1.35.0-linux-amd64.tar.gz | tar -xzv
  sudo mv ~/doctl /usr/local/bin
fi

doctl auth init -t "$DO_TOKEN"
doctl kubernetes cluster kubeconfig save "$K8S_ID"
