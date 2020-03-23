#!/usr/bin/env bash
# Exit if anycommand fails
set -e

CLIENT_NAME=${CLIENT_NAME:=$1}
REGION=${REGION:=europe-west4}
ZONE=${ZONE:=a}

TF_VAR_org_id=405354688018
TF_VAR_billing_account=00DB62-32FF8E-7DCFF1

cd deployments/terraform
terraform init
terraform workspace select ${CLIENT_NAME} || terraform workspace new ${CLIENT_NAME}
terraform destroy -var="project_name=${CLIENT_NAME}" -var="billing_account=${TF_VAR_billing_account}" -var="org_id=${TF_VAR_org_id}" -var="zone=${ZONE}" -var="region=${REGION}"