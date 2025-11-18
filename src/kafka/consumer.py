from kafka import KafkaConsumer
import json
from src.notifier.discord_notifier_bot import DiscordNotifier

consumer = KafkaConsumer(
    "wishlist_prices",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

notifier = DiscordNotifier()

for message in consumer:
    items = message.value

    msg = "**Wishlist atualizada:**\n"
    for item in items:
        msg += f"- {item['name']}: {item['price']}\n"

    notifier.send_message(msg)