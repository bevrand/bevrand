#!/usr/bin/env bash


../terraform init -backend-config="storage_account_name=$storage_account_name" -backend-config="access_key=$access_key"
../terraform taint tls_private_key.terraformusersshkey
../terraform taint digitalocean_droplet.docker
set -e
# Any subsequent(*) commands which fail will cause the shell script to exit immediately
../terraform plan -out outfile
../terraform apply -auto-approve outfile

export IP_ADDRESS_DROPLET=`../terraform output droplet_ip`
printenv IP_ADDRESS_DROPLET
export SSH_KEY_DEPLOY=`../terraform output private_ssh_key`
printenv SSH_KEY_DEPLOY

echo "Finished terraform run"
echo "Starting Ansible run"

printenv IP_ADDRESS_DROPLET
printenv SSH_KEY_DEPLOY

ip=$IP_ADDRESS_DROPLET
ssh_key=$SSH_KEY_DEPLOY

echo "Setting IP in ansible hosts to: [${ip}]"

echo "${ip}" >> ../ansible/hosts
echo 'Done setting ip in hosts'

ansible-playbook ../ansible/droplet_provision_centos.yml -i ../ansible/hosts --extra-vars "ssh_key=${ssh_key}"

echo 'Time to randomize'
