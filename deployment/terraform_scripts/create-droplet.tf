terraform {
  backend "azurerm" {
    container_name = "tfstate"
    key            = "prod.terraform.tfstate"
  }
}

variable "volume_id_data" {}

variable "do_token" {}

variable "docker_droplet_name" {
  default = "docker-terraform"
}

variable "droplet_image_name" {
  default = "docker"
}

variable "droplet_region" {
  default = "ams3"
}

variable "droplet_size" {
  default = "512mb"
}

variable "dev1_ssh_key_id" {}

variable "dev2_ssh_key_id" {}

variable "dev3_ssh_key_id" {}

provider "digitalocean" {
  token = "${var.do_token}"
}

module "firewall_inbound_cloudflare" {
  source = "andrewsomething/firewall-cloudflare/digitalocean"

  name = "inbound-cloudflare"
  tags = ["${digitalocean_tag.allow_inbound_cloudflare.name}"]
}

resource "digitalocean_tag" "allow_inbound_cloudflare" {
  name = "allow_inbound_cloudflare"
}

resource "digitalocean_tag" "sshmanagement" {
  name = "sshmanagement"
}

resource "digitalocean_firewall" "sshmanagementfirewall" {
  name = "sshmanagementfirewall"

  inbound_rule = [
    {
      protocol         = "tcp"
      port_range       = "22"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
  ]

  tags = ["${digitalocean_tag.sshmanagement.name}"]
}

resource "digitalocean_tag" "outboundall" {
  name = "outboundall"
}

resource "digitalocean_firewall" "outboundfirewall" {
  name = "outboundfirewall"

  outbound_rule = [
    {
      protocol              = "tcp"
      port_range            = "1-65535"
      destination_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol              = "udp"
      port_range            = "1-65535"
      destination_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol              = "icmp"
      port_range            = "1-65535"
      destination_addresses = ["0.0.0.0/0", "::/0"]
    },
  ]

  tags = ["${digitalocean_tag.outboundall.name}"]
}

resource "digitalocean_floating_ip" "docker" {
  droplet_id = "${digitalocean_droplet.docker.id}"
  region     = "${digitalocean_droplet.docker.region}"
}

#resource "null_resource" "generate_ssh_keys" {
#  provisioner "local-exec" {
#    command = "ssh-keygen -t ed25519 -f testingkey -N ''"
#    interpreter = ["sh"]
#  }
#}

resource "tls_private_key" "terraformusersshkey" {
  algorithm = "RSA"
}

# Add key to digital ocean !depend on generated ssh key
# Create a new SSH key
resource "digitalocean_ssh_key" "default" {
  name       = "terraformuser generated key"
  public_key = "${tls_private_key.terraformusersshkey.public_key_openssh}"
}

resource "digitalocean_droplet" "docker" {
  image      = "${var.droplet_image_name}"
  name       = "${var.docker_droplet_name}"
  region     = "${var.droplet_region}"
  size       = "${var.droplet_size}"
  ssh_keys   = ["${digitalocean_ssh_key.default.fingerprint}", "${var.dev1_ssh_key_id}", "${var.dev2_ssh_key_id}", "${var.dev3_ssh_key_id}"]
  user_data  = "${replace(file("cloud-config.conf"), "__sshkeygoeshere__", tls_private_key.terraformusersshkey.public_key_openssh)}"
  monitoring = true
  tags       = ["${digitalocean_tag.allow_inbound_cloudflare.name}", "${digitalocean_tag.sshmanagement.name}", "${digitalocean_tag.outboundall.name}"]
  volume_ids = ["${var.volume_id_data}"]

  connection {
    user        = "terraformuser"
    private_key = "${tls_private_key.terraformusersshkey.private_key_pem}"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo mkdir -p /mnt/datavolumedocker",
      "sudo mount -o discard,defaults /dev/disk/by-id/scsi-0DO_Volume_datavolumedocker /mnt/datavolumedocker",
      "sudo echo /dev/disk/by-id/scsi-0DO_Volume_datavolumedocker /mnt/datavolumedocker ext4 defaults,nofail,discard 0 0 | sudo tee -a /etc/fstab",
      "sudo docker run docker/whalesay cowsay Hello Bevrand",
      "sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "docker-compose --version",
      "sudo usermod -aG docker $USER",
      "cd /mnt/datavolumedocker/deployment/",
      "sudo docker-compose up -d",
      "sudo service ssh restart",                                                                                                                        #because we have the AllowUsers only on developer, this will permanently lock us out. Only do as the last thing
    ]
  }
}
