resource "google_pubsub_topic" "worker_topic" {
  name = var.PAGEVIEW_PUBSUB_TOPIC
}

resource "google_pubsub_subscription" "worker_sub" {
  name  = var.PAGEVIEW_PUBSUB_SUB
  topic = google_pubsub_topic.worker_topic.name

  message_retention_duration = "1200s"
  retain_acked_messages      = true
  ack_deadline_seconds       = 600
  expiration_policy {
    ttl = ""
  }
}
