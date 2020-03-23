locals {
 project_id = "${random_id.id.hex}"
}

resource "random_id" "id" {
 byte_length = 4
 prefix      = "${var.project_name}-"
}

resource "google_project" "project" {
 provider = "google-beta.google-beta"
 name            = local.project_id
 project_id      = local.project_id
 billing_account = "${var.billing_account}"
 org_id          = "${var.org_id}"
}


