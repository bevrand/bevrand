terraform {
  backend "azurerm" {
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

variable "volume_id_data" {}

variable "do_token" {}

variable "ssh_key_id" {}

variable "dev1_ssh_key_id" {}

variable "dev2_ssh_key_id" {}

variable "dev3_ssh_key_id" {}

variable "terraformuser_private_key" {}

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
  name       = "sshmanagementfirewall"

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
  name       = "outboundfirewall"

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

resource "digitalocean_droplet" "docker" {
  image      = "docker"
  name       = "docker-terraform"
  region     = "ams3"
  size       = "1gb"
  ssh_keys   = ["${var.ssh_key_id}", "${var.dev1_ssh_key_id}", "${var.dev2_ssh_key_id}", "${var.dev3_ssh_key_id}"]
  user_data  = "${file("cloud-config.conf")}"
  monitoring = true
  tags       = ["${digitalocean_tag.allow_inbound_cloudflare.name}", "${digitalocean_tag.sshmanagement.name}", "${digitalocean_tag.outboundall.name}"]
  volume_ids = ["${var.volume_id_data}"]

  connection {
    user        = "terraformuser"
    private_key = "${var.terraformuser_private_key}"
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
    ]
  }
}
