
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("./keys/my-creds.json")  # change this to your path
  project = "terraform-demo-449320"
  region  = "europe-west3" #  europe-west1 - London, europe-west4 - Netherlands
}

resource "google_storage_bucket" "data-lake-demo-bucket" {
  name          = "terraform-demo-449320-demo-terra-bucket" # it can be any name
  location      = "EU"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "demo_bigquery_dataset"
}
