# Stream processing pipeline

This codebase contains logic to simulate, ingest and process realtime data from various sources including kafka and pubsub. The diagram below provides a concise architecture of the pipeline.

![architecture](stream_processor.png)

## How this repository is organised

This repo has the following folder structure. `Poetry` was used to initialise folder structure.
📢 **Check the `data` folder for some sample outputs.**

```text
stream_processor
└───env
|   └───sa: Contains service account used by terraform and cloud services
└───infrastucture
|   └───scripts: Contains shell scripts for setting environment variables and running terraform
│   └───terraform: Contains all the modules required by terraform to provision the required infrastucture
└───stream_processor
|   └───beam: Contains codebase for pipelines created with the apache beam sdk
|   |   └───pipeline_utils: Contains utility functions used in the beam pipeline
|   |   └───schemas: Contains Json schema for data validation
|   |   └───data: Contains results from sample pipeline runs
|   └───publishers: Contains code for generating random data for both kafka and pubsub
|   └───tests
```
## Requirements and Assumptions
1. It is assumed that you have docker and docker-compose installed.
2. Create a google cloud project [here](https://cloud.google.com/free). The $300 free credit should be enough.
3. Edit the `GCP_PROJECT_ID` with the allocated project_id
4. Create a service account with an `Editor` role and download the service account key
5. Copy the key into `env/sa/sa_local.json`. You can also rename `dummy_file.json` to `sa_local.json` and paste in the key contents

## How to use
```bash
# Clone the public repository and cd into it
git clone https://github.com/opeoluwabanwo/stream_processor.git


# Create local dev. environment
make raise


# Provison GCP cloud infrastructure. This is required if
# the application is to be deployed on GCP.
make provision


# Run tests (unit and functional tests). The functional test essentially
# mocks the streaming data and runs the pipeline. Results are available in
# the results folder (fpattern is aggregates-*).
make run-tests


# Recommended for local (direct) runner
# This runs the stream processor app to consume pubsub messages and
# dumps the outputs into the results folder (pattern is beam-temp-*) in the root directory.
# Note that this is set to use directrunner if you want to run in the cloud
# remove the --runnner arg (default is set to DataflowRunner) and provide a bucket as # output path e.g --output_path gs://stream-processor/results.
make run-app-with-pubsub


# Not Recommended for local (direct) runner  due to issue https://issues.apache.org/jira/browse/BEAM-11991
# However it works using the DataflowRunnner. In this case, remove the --runnner arg (default is set to DataflowRunner) and provide a bucket as output path e.g --output_path gs://stream-processor/results
make run-app-with-kafka

# Stop container (terminates all processes)
make reset
```
📢 **Always check the `results` folder for output**

## Pending Issues
1. There is an open issue with using the local (direct) runner of the python sdk with the kafka read/write transforms tracked [here](https://issues.apache.org/jira/browse/BEAM-11991). However it works using the `DataflowRunnner`. In this case, remove the `--runnner` arg (default is set to DataflowRunner) and provide a bucket as output path e.g --output_path `gs://stream-processor/results`
