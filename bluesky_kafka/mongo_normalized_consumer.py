from functools import partial
import os

import msgpack
import msgpack_numpy as mpn

from bluesky_kafka import MongoBlueskyConsumer


bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
mongo_uri = os.environ.get("BLUESKY_MONGO_URI")
kafka_deserializer = partial(msgpack.loads, object_hook=mpn.decode)
auto_offset_reset = "latest"
topics = ["^.*bluesky.documents"]


# Create a MongoBlueskyConsumer that will automatically listen to new beamline topics.
# The parameter metadata.max.age.ms determines how often the consumer will check for
# new topics. The default value is 5000ms.
mongo_consumer = MongoBlueskyConsumer(
    topics=topics,
    bootstrap_servers=bootstrap_servers,
    group_id="kafka-unit-test-group-id",
    mongo_uri=mongo_uri,
    consumer_config={"auto.offset.reset": auto_offset_reset},
    polling_duration=1.0,
    deserializer=kafka_deserializer,
)


mongo_consumer.start()
