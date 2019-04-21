#!/usr/bin/env bash


../terraform init -backend-config="storage_account_name=$storage_account_name" -backend-config="access_key=$access_key"
../terraform taint tls_private_key.terraformusersshkey
../terraform taint digitalocean_droplet.docker
set -e
# Any subsequent(*) commands which fail will cause the shell script to exit immediately
../terraform plan -out outfile
../terraform apply -auto-approve outfile

export IP_ADDRESS_DROPLET=$(../terraform output droplet_ip)
export SSH_KEY_DEPLOY=$(../terraform output private_ssh_key)

echo "Finished terraform run"

sleep 30

echo "Starting Ansible run"

ip=$IP_ADDRESS_DROPLET
ssh_key=$SSH_KEY_DEPLOY

echo "Setting IP in ansible hosts to: [${ip}]"

echo "${ip}" >> ../ansible/hosts
echo 'Done setting ip in hosts'

echo "${ssh_key}" > id_rsa.pem
chmod 400 ./id_rsa.pem

ansible-playbook ../ansible/droplet_provision_centos.yml -i ../ansible/hosts --private-key=./id_rsa.pem --user terraformuser

echo 'Time to randomize'
