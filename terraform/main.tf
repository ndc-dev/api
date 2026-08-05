terraform {
  required_version = ">= 1.5.0"

  backend "gcs" {
    bucket = "ndc-dev-terraform-state"
    prefix = "api"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.40"
    }
  }
}

provider "google" {
  project = "ndc-dev-255301"
  region  = "asia-northeast1"
}

# 課金トラッキング用の共通ラベル
locals {
  common_labels = {
    service     = "api"
    environment = "production"
    managed-by  = "terraform"
  }
}

data "google_project" "current" {
  project_id = "ndc-dev-255301"
}
