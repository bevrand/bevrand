#!/usr/bin/env sh

ip=${IP_ADDRESS_DROPLET}
ssh_key=${SSH_KEY_DEPLOY}

echo ${ip}

echo "\n${ip}" >> ./ansible/hosts
echo 'Done setting ip in hosts'

ansible-playbook digitalocean.yml --extra-vars "ssh_key=${ssh_key}"

echo 'Time to randomize'
