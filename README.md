FHIR Patient Generator
=======================

## Pre requirements

see: https://cloud.google.com/community/tutorials/managing-gcp-projects-with-terraform

load variables from the tutorial into `setup-infra.sh`

TF_VAR_org_id=<YOUR-ORG-ID>
TF_VAR_billing_account=<YOUR-BILLING-ACCOUNT>

and provide terraform admin credentials into `tf-admin.json`

## Build and push

./build-api.sh <project_id>
 
## Deployment

./setup-infra.sh <project_name>

kustomize build deployments/manifests/ | kubectl apply -f -