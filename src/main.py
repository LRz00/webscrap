from src.scrapper.wishlist_scrapper import run_scrapper
from src.configs.config import config
from src.kafka.producer import publish_wishlist_update, close_producer

if __name__ == "__main__":
    try:
        url = config.get("wishlist_url", "")
        
        if not url:
            raise ValueError("wishlist_url is not configured in config.py")

        data = run_scrapper(url)

        if not data:
            print("Warning: No data scraped from wishlist")
            # Publish empty list to indicate successful scrape with no results
            publish_wishlist_update([])
        else:
            publish_wishlist_update(data)
            print("Data sent")
    except Exception as e:
        print(f"Error in main: {e}")
        raise
    finally:
        close_producer()