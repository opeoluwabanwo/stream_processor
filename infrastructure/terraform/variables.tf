
variable "GCP_PROJECT_ID" {}
variable "GCP_REGION" {}
variable "GCP_ZONE" {}
variable "GCP_REGION_MULTI" {}

variable "PAGEVIEW_PUBSUB_TOPIC" {}
variable "PAGEVIEW_PUBSUB_SUB" {}

variable "APPLICATION_NAME" {
  description = "Name of the deployed app"
  type        = string
}

variable "DATAFLOW_NETWORK" {
  type        = string
  description = "Name of the network for dataflow"
}

variable "DATAFLOW_SUBNETWORK" {
  type        = string
  description = "Name of the network for dataflow"
}

variable "DATAFLOW_NETWORK_CIDR" {
  type        = string
  default     = "10.2.0.0/16"
  description = "CIDR range for dataflow subnetwork"
}

variable "DATAFLOW_EXTERNAL_IP" {
  type        = string
  description = "static ip address name for the dataflow network"
}
