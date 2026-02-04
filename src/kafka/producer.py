from kafka import KafkaProducer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_wishlist_update(data):
    try:
        producer.send("wishlist_prices", value=data)
        producer.flush()
    except Exception as e:
        logger.error(f"Error publishing to Kafka: {e}")
        raise

def close_producer():
    """Close the Kafka producer to release resources"""
    try:
        producer.close()
    except Exception as e:
        logger.warning(f"Error closing Kafka producer: {e}")