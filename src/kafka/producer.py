from kafka import KafkaProducer
import json

from src.configs.config import config
from src.scrapper.wishlist_scrapper import run_scrapper

def create_producer():
    return KafkaProducer(
        bootstrap_servers = [config["kafka_broker"]],
        value_serializer= lambda v: json.dumps(v).encode("utf-8"),
        key_serializer= lambda k: str(k).encode("utf-8"),
    )

def send_wishlist_data():
    producer = create_producer()

    items = run_scrapper(config["wishlist_url"])

    for i, item in enumerate(items, 1):
        message_key = f"item_{i}"
        print(f"sending {item['name']} - R$ {item['price']}")
        producer.send(config["kafka_topic"], key=message_key, value=item);

    producer.flush();
    producer.close();