"""Unit tests for stream processor.

This module contains unit tests for various stages in the stream processing pipeline.
"""

import unittest
from json import dumps

import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

from stream_processor.beam.pipeline_utils.stream_processor_dofns import (
    FlatMapDofns,
    MessagePreprocessorDoFn,
)
from stream_processor.beam.schemas.pageview import SCHEMA_PAGEVIEW


class TestStreamProcessorDoFns(unittest.TestCase):
    """Unit tests for the stream processor pipeline."""

    # This is a fake dataset.
    SAMPLE_DATA = [
        {
            "user_id": 6170,
            "postcode": "N17",
            "webpage": "www.website.com/explore.html",
            "timestamp": 165530909,
        },
        {
            "user_id": 1244,
            "postcode": "E16",
            "webpage": "www.website.com/categories/category.html",
            "timestamp": 133136,
        },
        {
            "user_id": 7397,
            "postcode": "N17",
            "webpage": "www.website.com/blog.html",
            "timestamp": 426343704,
        },
        {
            "user_id": 3318,
            "postcode": "E16",
            "webpage": "www.website.com/categories.html",
            "timestamp": 647977659,
        },
        {
            "user_id": 2382,
            "postcode": "WC5",
            "webpage": "www.website.com/search/blog/blog.html",
            "timestamp": 726668099,
        },
        {
            "user_id": 1351,
            "postcode": "WC5",
            "webpage": "www.website.com/list.html",
            "timestamp": 956194597,
        },
        {
            "user_id": 3380,
            "postcode": "WC5",
            "webpage": "www.website.com/posts/main.html",
            "timestamp": 946844673,
        },
        {
            "user_id": 8656,
            "postcode": "WC5",
            "webpage": "www.website.com/main.html",
            "timestamp": 1121627593,
        },
        {
            "user_id": 2117,
            "postcode": "E16",
            "webpage": 1602572872,
            "timestamp": 1602572872,
        },
        {
            "user_id": 3599,
            "postcode": "N17",
            "webpage": "www.website.com/app.html",
            "timestamp": "bad_timestamp",
        },
    ]

    AGGREGATED_VIEWS = [
        {
            "aggregation_time": "2021-06-30 10:02:12.623220",
            "total_views": 2,
            "postcode": "N17",
        },
        {
            "aggregation_time": "2021-06-30 10:02:12.623220",
            "total_views": 2,
            "postcode": "E16",
        },
        {
            "aggregation_time": "2021-06-30 10:02:12.623220",
            "total_views": 4,
            "postcode": "WC5",
        },
    ]

    @classmethod
    def setUpClass(cls):
        """This sets up all fixtures needed for the tests."""
        cls.SAMPLE_STREAM = [
            (b"", dumps(pageview).encode("utf8")) for pageview in cls.SAMPLE_DATA
        ]
        cls.EXPECTED_AGGREGATED_VIEWS = [
            dumps(aggregate, sort_keys=True, default=str)
            for aggregate in cls.AGGREGATED_VIEWS
        ]

    def test_valid_messages_are_captured(self):
        """Test preprocessor dofn can capture valid messages."""
        with TestPipeline() as p:
            expected_valid_messages = self.SAMPLE_DATA[:8]
            messages = (
                p
                | "Read Sample Stream" >> beam.Create(self.SAMPLE_STREAM)
                | "Preprocess Stream"
                >> beam.ParDo(MessagePreprocessorDoFn(SCHEMA_PAGEVIEW)).with_outputs(
                    "valid", "invalid"
                )
            )
            assert_that(
                messages.valid,
                equal_to(expected_valid_messages),
                label="assert_valid_messages",
            )

    def test_invalid_messages_are_captured(self):
        """Test preprocessor dofn can capture invalid messages."""
        with TestPipeline() as p:
            expected_invalid_messages = self.SAMPLE_DATA[-2:]
            messages = (
                p
                | "Read Sample Stream" >> beam.Create(self.SAMPLE_STREAM)
                | "Preprocess Stream"
                >> beam.ParDo(MessagePreprocessorDoFn(SCHEMA_PAGEVIEW)).with_outputs(
                    "valid", "invalid"
                )
            )

            assert_that(
                messages.invalid,
                equal_to(expected_invalid_messages),
                label="assert_invalid_messages",
            )

    def test_aggregates_are_properly_computed(self):
        """Test that aggregation feature is correct."""
        with TestPipeline() as p:
            sample_window = [(None, self.SAMPLE_DATA[:8])]
            results = (
                p
                | "Create window" >> beam.Create(sample_window)
                | "Aggregate PageViews"
                >> beam.FlatMap(
                    FlatMapDofns.aggregate_pageviews,
                    window="2021-06-30 10:02:12.623220",
                )
            )

            assert_that(
                results,
                equal_to(self.EXPECTED_AGGREGATED_VIEWS),
                label="assert_expected_aggregate_results",
            )
