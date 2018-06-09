#!/usr/bin/env sh


../terraform init
../terraform taint digitalocean_droplet.docker
../terraform plan -out outfile
../terraform apply -auto-approve outfile

