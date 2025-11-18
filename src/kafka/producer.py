from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_wishlist_update(data):
    producer.send("wishlist_prices", value=data)
    producer.flush()