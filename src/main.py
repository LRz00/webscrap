from src.scrapper.wishlist_scrapper import run_scrapper
from src.configs.config import config
from src.kafka.producer import publish_wishlist_update

if __name__ == "__main__":
    url = config["wishlist_url"]

    data = run_scrapper(url)

    publish_wishlist_update(data)

    print("Data sent")