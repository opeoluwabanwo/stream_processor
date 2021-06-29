import os
import threading
import time

from google.cloud import pubsub

from stream_processor.publishers.data_generator import RandomDataGenerator


class Publisher(threading.Thread):
    def __init__(self, input_topic):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self._publisher = pubsub.PublisherClient()
        self._input_topic = input_topic
        self._data_generator = RandomDataGenerator("en_GB")

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            pageview = self._data_generator.generate_pageview()
            self._publisher.publish(self._input_topic, pageview, encoding="utf8")
            time.sleep(5)

if __name__ == "__main__":
    project = os.getenv("GCP_PROJECT_ID")
    TOPIC = f"projects/{project}/topics/topic_pageviews"
    producer = Publisher(input_topic=TOPIC)
    producer.start()
    time.sleep(100)
    producer.stop()
    producer.join
