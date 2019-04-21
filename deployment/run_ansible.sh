#!/usr/bin/env bash

echo "Starting Ansible run"

printenv IP_ADDRESS_DROPLET
printenv SSH_KEY_DEPLOY

ip=$IP_ADDRESS_DROPLET
ssh_key=$SSH_KEY_DEPLOY

echo "Setting IP in ansible hosts to: [${ip}]"

echo "\n${ip}" >> ../ansible/hosts
echo 'Done setting ip in hosts'

ansible-playbook ../ansible/droplet_provision_centos.yml --extra-vars "ssh_key=${ssh_key}"

echo 'Time to randomize'
