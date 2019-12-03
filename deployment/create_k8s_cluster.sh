#!/usr/bin/env bash

set -e

CUR_DIR=$(cd "$( dirname -- "${BASH_SOURCE[0]}" )" && pwd)

dir=$1
if [[ -z "$1" ]]; then
  echo "Missing mandatory argument directory"
  exit
fi

cd "$CUR_DIR"/terraform_scripts/"${dir}"/

if [[ -z $2 ]]; then
    token=$DO_TOKEN
else
  token=$2
fi

if [[ -z "$token" ]]; then
  echo "Missing mandatory argument token. Either set DO_TOKEN as env variable or pass in as argument"
  exit
fi

terraform init
#set -e
## Any subsequent(*) commands which fail will cause the shell script to exit immediately
terraform plan -var "do_token=${token}" -out outfile
terraform apply -auto-approve outfile

k8s_id=$(terraform output k8s_id)
export K8S_ID=$k8s_id

. "$CUR_DIR/terraform_scripts/"${dir}"/deploy-k8s.sh"


export ENV_TARGET=cloud

. "$CUR_DIR/kubernetes/helm/deploy.sh"
