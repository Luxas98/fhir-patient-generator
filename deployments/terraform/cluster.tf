resource "google_container_cluster" "primary" {
  provider = "google-beta.google-beta-project"
  name     = "${google_project.project.project_id}"
  location = "${var.region}-${var.zone}"
  project     = "${google_project.project.project_id}"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count = 1

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = true
    }
  }

  # This enables IP-aliasing
  ip_allocation_policy {}

  depends_on = [google_project_service.project-container-service]
}

resource "google_container_node_pool" "service-pool" {
  provider = "google-beta.google-beta-project"
  name       = "service-pool"
  location   = "${var.region}-${var.zone}"
  cluster    = "${google_container_cluster.primary.name}"
  initial_node_count = 1 # Pulsar requires at least 3 running nodes
  project     = "${google_project.project.project_id}"

  management {
    auto_upgrade = false
  }

  node_config {
    preemptible  = false
    machine_type = "n1-standard-2"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/devstorage.full_control",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring"
    ]
  }

  depends_on = [google_project_service.project-container-service]
}