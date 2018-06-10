#!/usr/bin/env sh


../terraform init -backend-config="storage_account_name=$storage_account_name" -backend-config="access_key=$access_key"
../terraform taint tls_private_key.terraformusersshkey
../terraform taint digitalocean_droplet.docker
../terraform plan -out outfile
../terraform apply -auto-approve outfile
