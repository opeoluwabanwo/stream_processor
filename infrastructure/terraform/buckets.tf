resource "google_storage_bucket" "gcs_bucket_dataflow" {
  name          = "${var.APPLICATION_NAME}-dataflow"
  location      = var.GCP_REGION
  storage_class = "REGIONAL"
  force_destroy = false
}
