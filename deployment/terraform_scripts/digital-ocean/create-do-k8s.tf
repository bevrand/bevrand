variable "do_token" {}

variable "k8s_name" {
  type        = string
  description = "cluster name as known by DO"
  default = "bevrand-k8s"
}

variable "k8s_region" {
  type        = string
  description = "hosted region"
  default = "ams3"
}

variable "k8s_version" {
  type        = string
  description = "DO specified version"
  default = "1.16.2-do.0"
}

variable "node_name" {
  type        = string
  description = "node name as known by DO"
  default = "k8s-pool"
}

variable "node_size" {
  type        = string
  description = "node name as known by DO"
  default = "s-1vcpu-2gb"
}

variable "node_count" {
  type        = number
  description = "number of workers in de node pool"
  default = 2
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_kubernetes_cluster" "kubernetes" {
  name    = var.k8s_name
  region  = var.k8s_region
  version = var.k8s_version

  node_pool {
    name       = var.node_name
    size       = var.node_size
    node_count = var.node_count
  }
}

output "k8s_id" {
  value = digitalocean_kubernetes_cluster.kubernetes.id
}