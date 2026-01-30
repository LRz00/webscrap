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
    try:
        items = message.value
        if not isinstance(items, list):
            print(f"Warning: Expected list of items, got {type(items)}")
            continue
        
        changes = []

        with engine.begin() as conn:
            for item in items:
                if not isinstance(item, dict):
                    print(f"Warning: Expected dict item, got {type(item)}")
                    continue
                    
                item_name = item.get("name", item.get("product_name", "Unknown"))
                price_str = item.get("price", "0")
                
                # Handle price parsing safely
                try:
                    item_price = float(price_str.replace("R$", "").replace(",", ".").strip())
                except (ValueError, AttributeError):
                    print(f"Warning: Invalid price format for item {item_name}: {price_str}")
                    continue

                result = conn.execute(GET_LAST_PRICE_QUERY, {"product_name": item_name})
                row = result.fetchone()
                if row is not None:

                    old_price = float(row[0])
                    # Prevent division by zero
                    if old_price != 0:
                        variation = ((item_price - old_price) / old_price * 100)
                        if abs(variation) >= PERCENTUAL_THRESHOLD:
                            changes.append(
                                    f"- {item_name}: {old_price:.2f} → {item_price:.2f} "
                                    f"({variation:+.2f}%)"
                                )
                    elif item_price != old_price:
                        # Handle case where old price was 0
                        changes.append(
                                f"- {item_name}: {old_price:.2f} → {item_price:.2f} (new price)"
                            )
                conn.execute(INSERT_PRICE_QUERY, {"product_name": item_name, "price": item_price})
                
        if changes:
            msg = "⚠️ **Price Changes Detected:**\n" + "\n".join(changes) 
            try:
                notifier.send_message(msg)
            except Exception as e:
                print(f"Error sending notification: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")
        # Continue processing next messages instead of crashing