terraform {
  required_version = ">= 0.13"

  required_providers {
    google = {
      version = "~> 3.51.0"
      source  = "hashicorp/google"
    }
    archive = {
      version = "~> 2.0.0"
      source  = "hashicorp/archive"
    }
  }
}
