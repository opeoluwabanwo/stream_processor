resource "google_compute_network" "dataflow" {
  name                    = var.DATAFLOW_NETWORK
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "dataflow" {
  name                     = var.DATAFLOW_SUBNETWORK
  ip_cidr_range            = var.DATAFLOW_NETWORK_CIDR
  region                   = var.GCP_REGION
  network                  = google_compute_network.dataflow.id
  private_ip_google_access = true
}

resource "google_compute_firewall" "dataflow_access" {
  name    = "${google_compute_network.dataflow.name}-internal-access"
  network = google_compute_network.dataflow.name

  direction   = "INGRESS"
  priority    = 0
  source_tags = ["dataflow"]
  target_tags = ["dataflow"]

  allow {
    protocol = "tcp"
    ports    = ["12345-12346"]
  }
}

resource "google_compute_router" "dataflow" {
  name    = "${google_compute_network.dataflow.name}-router"
  region  = google_compute_subnetwork.dataflow.region
  network = google_compute_network.dataflow.id
}

resource "google_compute_router_nat" "dataflow_nat" {
  name                               = "${google_compute_network.dataflow.name}-nat-router"
  router                             = google_compute_router.dataflow.name
  region                             = google_compute_router.dataflow.region
  nat_ip_allocate_option             = "MANUAL_ONLY"
  nat_ips                            = google_compute_address.dataflow_static_ip.*.self_link
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

resource "google_compute_address" "dataflow_static_ip" {
  name   = var.DATAFLOW_EXTERNAL_IP
  region = var.GCP_REGION
}
