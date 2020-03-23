resource "google_project_service" "compute-service" {
 project = "${google_project.project.project_id}"
 service = "compute.googleapis.com"
 disable_dependent_services = false
 disable_on_destroy = false
 provider = "google-beta.google-beta-project"
}

resource "google_project_service" "project-container-service" {
 project = "${google_project.project.project_id}"
 service = "container.googleapis.com"
 disable_dependent_services = false
 disable_on_destroy = false
 provider = "google-beta.google-beta-project"
}