from kafka import KafkaConsumer
import json
from src.notifier.discord_notifier_bot import DiscordNotifier
from sqlalchemy import text
from src.db.db import engine

PERCENTUAL_THRESHOLD = 5.0

consumer = KafkaConsumer(
    "wishlist_prices",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

notifier = DiscordNotifier()

GET_LAST_PRICE_QUERY = text("""
    SELECT price 
    FROM price_history                            
    WHERE product_name = :product_name
    ORDER BY recorded_at DESC
    LIMIT 1
""")

INSERT_PRICE_QUERY = text("""
    INSERT INTO price_history (product_name, price)
    VALUES (:product_name, :price)               
""")


for message in consumer:
    items = message.value
    changes = []

    with engine.begin() as conn:
        for item in items:
            item_name = item["product_name"]
            item_price = float(item["price"].replace("R$", "").replace(",", ".").strip())

            result = conn.execute(GET_LAST_PRICE_QUERY, {"product_name": item_name})
            row = result.fetchone()
            if row is not None:

                old_price = float(row[0])
                variation = ((item_price - old_price) / old_price * 100)
                if abs(variation) >= PERCENTUAL_THRESHOLD:
                    changes.append(
                            f"- {item_name}: {old_price:.2f} → {item_price:.2f} "
                            f"({variation:+.2f}%)"
                        )
            conn.execute(INSERT_PRICE_QUERY, {"product_name": item_name, "price": item_price})
            
    if changes:
        msg = "⚠️ **Price Changes Detected:**\n" + "\n".join(changes) 
        notifier.send_message(msg)