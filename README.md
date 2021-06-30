# Stream processing pipeline

This codebase contains logic to simulate, ingest and process realtime data from various sources including kafka and pubsub.

## How this repository is organised

This repo has the following folder structure. `Poetry` was used to initialise folder structure.

```text
stream_processor
└───infrastucture
|   └───scripts: Contains shell scripts for setting environment variables and running terraform
│   └───terraform: Contains all the modules required by terraform to provision the required infrastucture
└───stream_processor
|   └───beam: Contains codebase for pipelines created with the apache beam sdk
|   |   └───pipeline_utils: Contains utility functions used in the beam pipeline
|   |   └───schemas: Contains Json schema for data validation
|   └───publishers: Contains code for generating random data for both kafka and pubsub
|   └───tests
```
## Requirements and Assumptions
1. It is assumed that you have docker and docker-compose installed.
2. Create a google cloud project [here](https://cloud.google.com/free). The $300 free credit should be enough.
3. Create a service account with an `Editor` role and download the service account key
4. Copy the key into `env/sa/sa_local.json`. Note the folder names and create if needed
 
## How to use
📢 **Always check the `results` folder for output**

```bash
# Create local dev. environment
make raise

# Provison GCP cloud infrastructure. This is required if
# the application is to be deployed on GCP.
make provision

# Run tests (unit and functional tests). The functional test essentially
# mocks the streaming data and runs the pipeline. Results are available in
# the results folder (for instance aggregates-*).
make run-tests

# Recommended for local (direct) runner
# This runs the stream processor app to consume pubsub messages and
# dumps the outputs into the results folder in the root directory.
# Note that this is set to use directrunner if you want to run in the cloud
# remove the --runnner arg (default is set to DataflowRunner) and provide a bucket as # output path e.g --output_path gs://stream-processor/results.
make run-app-with-pubsub

# Not Recommended for local (direct) runner  due to issue https://issues.apache.org/jira/browse/BEAM-11991
# However it works using the DataflowRunnner. In this case, remove the --runnner arg (default is set to DataflowRunner) and provide a bucket as output path e.g --output_path gs://stream-processor/results
make run-app-with-kafka
```

## Pending Issues
1. There is an open issue with using the local (direct) runner  with the python sdk due tracked [here](https://issues.apache.org/jira/browse/BEAM-11991). However it works using the `DataflowRunnner`. In this case, remove the `--runnner` arg (default is set to DataflowRunner) and provide a bucket as output path e.g --output_path `gs://stream-processor/results`