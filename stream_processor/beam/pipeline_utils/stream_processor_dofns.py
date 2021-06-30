"""Distributed functions for the stream processing pipeline.

This module contains logic for all distributed functions used
within the stream processing pipeline.
"""
import random
from collections import defaultdict
from datetime import datetime
from json import dumps, loads

from apache_beam import DoFn, GroupByKey, PTransform, TaggedOutput, WindowInto, WithKeys
from apache_beam.transforms.window import FixedWindows
from faker import Faker
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class GroupMessagesByFixedWindows(PTransform):
    """A composite transform that groups messages based on publish time
    and outputs a list of tuples, each containing a message and partition key.
    """

    def __init__(self, window_size, num_shards=5):
        # Set window size to 60 seconds.
        self.window_size = int(window_size * 60)
        self.num_shards = num_shards

    def expand(self, pcoll):
        return (
            pcoll
            | "Window into fixed intervals"
            >> WindowInto(FixedWindows(self.window_size))
            # Assign a random key to each window based on the number of shards.
            | "Add key" >> WithKeys(lambda _: random.randint(0, self.num_shards - 1))
            | "Group by key" >> GroupByKey()
        )


class MessagePreprocessorDoFn(DoFn):
    """Validates and decodes messages from the stream."""

    def __init__(self, schema):
        """Initialise the message preprocessor."""
        self._schema = schema
        DoFn.__init__(self)

    def process(self, message):
        """Decode and validate message against schema."""
        _, message_value = message
        pageview = loads(message_value)
        try:
            validate(pageview, self._schema)
            yield TaggedOutput("valid", pageview)
        except ValidationError:
            yield TaggedOutput("invalid", pageview)


class FlatMapDofns:
    """Encapsulates functions used within map and flatmap transfroms."""

    @staticmethod
    def aggregate_pageviews(
        batch, streaming_engine="local", window=DoFn.TimestampParam
    ):
        """Pivots and aggregates messages captured in a window."""
        # Compute the window i.e. aggregation timestamp
        if isinstance(window, str):
            aggregation_time = window
        else:
            ts_format = "%Y-%m-%d %H:%M:%S.%f"
            if streaming_engine == "local":
                aggregation_time = datetime.now().strftime(ts_format)
            else:
                aggregation_time = datetime.utcfromtimestamp(float(window)).strftime(
                    ts_format
                )

        # Compute total views per postcode
        total_views_per_postcode = defaultdict(int)
        _, pageviews = batch
        for pageview in pageviews:
            postcode = pageview["postcode"]
            total_views_per_postcode[postcode] += 1

        # Emit aggregate results
        for postcode, total_views in total_views_per_postcode.items():
            result = {
                "postcode": postcode,
                "aggregation_time": aggregation_time,
                "total_views": total_views,
            }
            yield dumps(result, sort_keys=True, default=str)

    @staticmethod
    def generate_pageviews():
        """Generates random stream of messages for testing."""
        fake = Faker("en_GB")
        for _ in range(100):
            webpage = f"www.website.com/{fake.uri_path()}.html"
            postcode = fake.postcode().split()[0]
            # This reduces the sample postcode space inorder to enable
            # proper testing otherwise most post pageviews will be
            # aggregated to 1.
            # postcode = fake.random_element(("SW8", "E16", "WC5", "N17"))
            data = {
                "user_id": fake.random_int(),
                "postcode": postcode,
                "webpage": webpage,
                "timestamp": fake.unix_time(),
            }
            yield (b"", dumps(data).encode("utf-8"))
