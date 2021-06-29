#!/bin/bash

echo $(tput bold)$(tput setab 1)$(tput setaf 7)CONFIG$(tput sgr 0)

# Environment variables (scope is this script)

export APPLICATION_NAME="stream-processor"
export GCP_REGION="europe-west2"
export GCP_ZONE="europe-west2-b"
export GCP_REGION_MULTI="EU"
export GCP_PROJECT_ID="lateral-balm-318212"

# Dataflow Configuratiom
export MACHINE_TYPE="n1-standard-1"
export PIPELINE_RUNNER="DataflowRunner"
export DATAFLOW_NETWORK="dataflow-network"
export DATAFLOW_EXTERNAL_IP="static-ip-dataflow"
export DATAFLOW_SUBNETWORK="$DATAFLOW_NETWORK-$GCP_REGION"


export SCRIPT_PATH="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 ; pwd -P )"
export PATH_HOME=$(dirname $(dirname $SCRIPT_PATH))
export PATH_ENV=${PATH_HOME}/env
export PATH_SA_KEY=${PATH_ENV}/sa/sa_local.json
export PATH_TF=${PATH_HOME}/infrastructure/terraform


# Staging Bucket for Dataflow
export GCS_BUCKET_DATAFLOW="${APPLICATION_NAME}-dataflow"

# TF Environment Variables
export TF_VAR_APPLICATION_NAME=${APPLICATION_NAME}
export TF_VAR_PATH_SA_KEY=${PATH_SA_KEY}

export TF_VAR_GCP_PROJECT_ID=${GCP_PROJECT_ID}
export TF_VAR_GCP_REGION=${GCP_REGION}
export TF_VAR_GCP_REGION_MULTI=${GCP_REGION_MULTI}
export TF_VAR_GCP_ZONE=${GCP_ZONE}

export TF_VAR_DATAFLOW_EXTERNAL_IP=${DATAFLOW_EXTERNAL_IP}
export TF_VAR_DATAFLOW_NETWORK=${DATAFLOW_NETWORK}
export TF_VAR_DATAFLOW_SUBNETWORK=${DATAFLOW_SUBNETWORK}

export TF_VAR_PAGEVIEW_PUBSUB_TOPIC="topic_pageviews"
export TF_VAR_PAGEVIEW_PUBSUB_SUB="sub_pageviews"

# Gcloud Config & Credentials
gcloud auth activate-service-account --key-file=${PATH_SA_KEY}
export GOOGLE_APPLICATION_CREDENTIALS=${PATH_SA_KEY}

gcloud config set project ${GCP_PROJECT_ID}
gcloud config set compute/region ${GCP_REGION}
gcloud config set compute/zone ${GCP_ZONE}
