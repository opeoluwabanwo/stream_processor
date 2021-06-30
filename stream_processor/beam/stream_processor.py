import argparse
import logging
import typing

from apache_beam import Create, DoFn, FlatMap, Map, ParDo, Pipeline, io
from apache_beam.io.kafka import ReadFromKafka
from pipeline_utils.pipeline_options_builder import PipelineOptionsBuilder
from pipeline_utils.stream_processor_dofns import (
    FlatMapDofns,
    GroupMessagesByFixedWindows,
    MessagePreprocessorDoFn,
)
from schemas.pageview import SCHEMA_PAGEVIEW


def run(
    input_topic,
    output_path,
    streaming_engine,
    window_size,
    num_shards,
    pipeline_args=None,
):
    pipeline_options = PipelineOptionsBuilder.build_pipe_options(
        pipeline_args, "pageview-processor"
    )

    with Pipeline(options=pipeline_options) as pipeline:
        if streaming_engine == "kafka":
            messages = (
                pipeline
                | "Read messages from Kafka"
                >> ReadFromKafka(
                    consumer_config={"bootstrap.servers": "localhost:9092"},
                    topics=[input_topic],
                ).with_output_types(typing.Tuple[bytes, bytes])
            )
        elif streaming_engine == "pubsub":
            subscription_path = (
                f"projects/{pipeline_options.project}/subscriptions/sub_pageviews"
            )
            messages = (
                pipeline
                | "Read messages from PubSub"
                >> io.ReadFromPubSub(subscription=subscription_path)
                # Simulate message structure expected by kafka
                | "Append Keys"
                >> Map(lambda message: (b"", message)).with_output_types(
                    typing.Tuple[bytes, bytes]
                )
            )
        # Simulate a local Pcollection of sample messages
        else:
            messages = pipeline | "Read messages from Kafka" >> Create(
                FlatMapDofns.generate_pageviews()
            ).with_output_types(typing.Tuple[bytes, bytes])

        decoded_messages = messages | "Decode and validate messages" >> ParDo(
            MessagePreprocessorDoFn(SCHEMA_PAGEVIEW)
        ).with_outputs("valid", "invalid")

        _ = decoded_messages.valid | "Write Stream to GCS/Local " >> io.WriteToText(
            f"{output_path}/passthrough"
        )
        _ = (
            decoded_messages.valid
            | "Group Messages" >> GroupMessagesByFixedWindows(window_size, num_shards)
            | "Aggregate PageViews"
            >> FlatMap(FlatMapDofns.aggregate_pageviews, streaming_engine)
            | "Write Aggregates to GCS/Local "
            >> io.WriteToText(f"{output_path}/aggregates")
        )

        _ = (
            decoded_messages.invalid
            # In production this should be recycled to a hospital/dead-letter topic
            | "Write Bad Records to GCS/Local"
            >> io.WriteToText(f"{output_path}/bad_records")
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_topic", default="topic_pageviews", help="The topic to stream from."
    )
    parser.add_argument(
        "--streaming_engine",
        default="pubsub",
        help="Streaming engine to use.",
    )
    parser.add_argument(
        "--window_size",
        type=float,
        default=0.1,
        help="Window size in minutes.",
    )
    parser.add_argument(
        "--output_path",
        default="./results",
        help="Path of the output artefacts (GCS/Local)",
    )
    parser.add_argument(
        "--num_shards",
        type=int,
        default=5,
        help="Number of shards to use for partitioning groups",
    )
    known_args, pipeline_args = parser.parse_known_args()

    run(
        known_args.input_topic,
        known_args.output_path,
        known_args.streaming_engine,
        known_args.window_size,
        known_args.num_shards,
        pipeline_args,
    )
