resource "google_service_account" "client-sa" {
  project = "${google_project.project.project_id}"
  account_id   = "${google_project.project.project_id}"
  display_name = "${var.project_name}"
  provider = "google-beta.google-beta-project"
}

resource "google_service_account_key" "google_storage_access" {
  provider = "google-beta.google-beta-project"
  service_account_id = "${google_service_account.client-sa.name}"
}

resource "kubernetes_secret" "google-application-credentials" {
  provider = "kubernetes.primary"
  metadata {
    name = "google-application-credentials"
  }
  data = {
    "credentials.json" = base64decode(google_service_account_key.google_storage_access.private_key)
  }
}

resource "local_file" "gcs-credentials" {
    content     = base64decode(google_service_account_key.google_storage_access.private_key)
    filename = "${path.module}/credentials.json"
}
