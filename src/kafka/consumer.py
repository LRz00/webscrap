import redis
from kafka import KafkaConsumer
import json
from src.configs.config import config
def connect_redis():
    return redis.Redis(
        host=config["redis_host"],
        port=config["redis_port"],
        decode_responses=True
    )


def create_consumer():
    return KafkaConsumer(
        config["kafka_topic"],
        bootstrap_servers=config["kafka_broker"],
        value_deserialize=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="wishlist-alerts"
    )


def check_variation(item_name, new_price, r):
    last_price = r.get(item_name);

    try:
        new_price = float(str(new_price).replace(",", "."))
    except ValueError:
        print(f"Invalid price")
        return
    

    if last_price:
        last_price = float(last_price)
        variation = ((last_price - new_price) / last_price) * 100

        if variation >= 5:
            #send alert
            print(f"alert")
    
    r.set(item_name, new_price)


def consume_messages():
    print(f"Consumer started listening to prices")
    consumer = create_consumer()
    r = connect_redis()

    for msg in consumer:
        item = msg.value
        name = item.get("name")
        price = item.get("price")

        if not name or not price or price == "N/A" or name == "N/A":
            continue
        
        check_variation(name, price, r)