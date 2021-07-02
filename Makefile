ifndef VERBOSE
MAKEFLAGS += --no-sprint-directory
endif

SHELL  := /bin/bash
PYTHON := /usr/bin/env python3

raise: ## Create local container e.g. make raise region=eu env=dev
	@echo "# Create local container (can take a few mins)"
	docker build -t stream-processor-img .
	docker rm -f stream-processor-cont
	docker run -itd --network=host --name stream-processor-cont --volume ${PWD}:/app/ stream-processor-img

## Provison GCP cloud infrastructure. This is required if
## the application is to be deployed on GCP.
provision:
	@echo "# Provison GCP cloud infrastructure i.e. dataflow, buckets and pubsub"
	docker exec stream-processor-cont bash -c 'cd /app/infrastructure/scripts && ./provision.sh'

## Run tests (unit and functional tests). The functional test essentially
## mocks the streaming data and runs the pipeline. Results are available in
## the results folder (for instance aggregates-*).
run-tests:
	@echo "# Running unit tests"
	docker exec stream-processor-cont bash -c 'pytest /app/tests'
	@echo "# Running functional test (mocks the data stream)"
	docker exec stream-processor-cont bash -c 'python /app/stream_processor/beam/stream_processor.py --runner DirectRunner --streaming_engine local'

## Recommended for local (direct) runner
## This runs the stream processor app to consume pubsub messages and
## dumps the outputs into the results folder in the root directory.
## Note that this is set to use directrunner if you want to run in the cloud
## remove the --runnner arg (default is set to DataflowRunner) and provide a bucket as ## output path e.g --output_path gs://stream-processor/results.
run-app-with-pubsub:
	@echo "# Start the Pubsub publisher"
	docker exec --detach stream-processor-cont bash -c 'cd /app/infrastructure/scripts && source config.sh && python /app/stream_processor/publishers/pubsub_publisher.py'

	@echo "# Run the stream processor app (consumes pubusb messsages)"
	docker exec stream-processor-cont bash -c 'cd /app/infrastructure/scripts && source config.sh && cd /app && python stream_processor/beam/stream_processor.py --runner DirectRunner --streaming_engine pubsub'


## Not Recommended for local (direct) runner  due to issue https://issues.apache.org/jira/browse/BEAM-11991
## However it works using the DataflowRunnner. In this case, remove the --runnner arg (default is set to DataflowRunner) and provide a bucket as output path e.g --output_path gs://stream-processor/results
run-app-with-kafka:
	@echo "# Create local kafka stack"
	cd ./infrastructure && docker compose down && docker compose up -d
	@echo "# Start the kafka producer"
	docker exec --detach stream-processor-cont bash -c 'python /app/stream_processor/publishers/kafka_publisher.py'

	@echo "# Run the stream processor app (consumes kafka messsages)"
	docker exec stream-processor-cont bash -c 'cd /app/infrastructure/scripts && source config.sh && cd /app && python stream_processor/beam/stream_processor.py --runner DirectRunner --streaming_engine kafka'

reset: ## Stop container (terminates all processes)
	@echo "# Stop running container"
	docker rm -f stream-processor-cont

.PHONY: help raise reset run-tests
help:
	@grep -hE '^[a-zA-Z0-9\._/-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
