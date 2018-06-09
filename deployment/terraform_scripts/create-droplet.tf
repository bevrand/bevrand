variable "do_token" {}

variable "key_path" {
  default = "/home/joerivrij/.ssh/id_rsa"
}

variable "ssh_key_id" {
  default = "fb:9d:2f:52:96:0f:22:4a:44:af:40:99:ee:91:a1:ad"
}

provider "digitalocean" {
  token = "${var.do_token}"
}

module "firewall_inbound_cloudflare" {
  source = "andrewsomething/firewall-cloudflare/digitalocean"

  name = "inbound-cloudflare"
  tags = ["allow_inbound_cloudflare"]
}

resource "digitalocean_tag" "allow_inbound_cloudflare" {
  name = "allow_inbound_cloudflare"
}

resource "digitalocean_tag" "sshmanagement" {
  name = "sshmanagement"
}

resource "digitalocean_firewall" "sshmanagementfirewall" {
  name       = "sshmanagementfirewall"
  depends_on = ["digitalocean_tag.sshmanagement"]

  inbound_rule = [
    {
      protocol         = "tcp"
      port_range       = "22"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
  ]

  tags = ["sshmanagement"]
}

resource "digitalocean_tag" "outboundall" {
  name = "outboundall"
}

resource "digitalocean_firewall" "outboundfirewall" {
  name       = "outboundfirewall"
  depends_on = ["digitalocean_tag.outboundall"]

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

  tags = ["outboundall"]
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
  ssh_keys   = ["${var.ssh_key_id}"]
  user_data  = "${file("cloud-config.conf")}"
  monitoring = true
  tags       = ["${digitalocean_tag.allow_inbound_cloudflare.name}", "${digitalocean_tag.sshmanagement.name}", "${digitalocean_tag.outboundall.name}"]
  volume_ids = ["c8ace9bc-6bfc-11e8-bbbe-0242ac114a0a"]

  connection {
    user        = "terraformuser"
    private_key = "${file(var.key_path)}"
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
