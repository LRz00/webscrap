from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_wishlist_update(data):
    try:
        producer.send("wishlist_prices", value=data)
        producer.flush()
    except Exception as e:
        print(f"Error publishing to Kafka: {e}")
        raise

def close_producer():
    """Close the Kafka producer to release resources"""
    try:
        producer.close()
    except Exception as e:
        print(f"Error closing Kafka producer: {e}")