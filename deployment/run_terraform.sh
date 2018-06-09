#!/usr/bin/env sh


../terraform init
../terraform plan -out outfile
../terraform apply -auto-approve outfile

