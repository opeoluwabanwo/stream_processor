terraform {
  backend "local" {
    path = "states/terraform.tfstate"
  }
}

variable "PATH_SA_KEY" {
  description = "Path to the default compute engine service account key."
  type        = string
}


provider "google" {
  credentials = file(var.PATH_SA_KEY)

  # Should be able to parse project from credentials file but cannot.
  # Cannot convert string to map and cannot interpolate within variables.
  project = var.GCP_PROJECT_ID
  region  = var.GCP_REGION
}
