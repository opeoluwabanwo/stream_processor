echo $(tput bold)$(tput setab 1)$(tput setaf 7)PROVISION:tf ${APPLICATION_NAME}$(tput sgr 0)

# Configure environment variables
source config.sh

# Ensure required api services are enabled
gcloud services enable \
    iamcredentials.googleapis.com \
    serviceusage.googleapis.com \
    cloudresourcemanager.googleapis.com \
    dataflow.googleapis.com \
    iamcredentials.googleapis.com \
    stackdriver.googleapis.com \
    monitoring.googleapis.com

# Apply terraform modules
cd ${PATH_TF}

terraform init -reconfigure -backend-config=${PATH_TF_CONFIG}

terraform plan
terraform apply -auto-approve
