import threading
import time

from data_generator import RandomDataGenerator
from kafka import KafkaProducer


class Producer(threading.Thread):
    def __init__(self, servers, input_topic):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self._servers = servers
        self._input_topic = input_topic
        self._data_generator = RandomDataGenerator("en_GB")

    def stop(self):
        self._stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers=self._servers)

        while not self._stop_event.is_set():
            pageview = self._data_generator.generate_pageview()
            producer.send(self._input_topic, b"", pageview)
            time.sleep(0.1)
        producer.close()


if __name__ == "__main__":
    producer = Producer(servers="localhost:9092", input_topic="topic_pageviews")
    producer.start()
    time.sleep(100)
    producer.stop()
    producer.join
