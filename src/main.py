from src.scrapper.wishlist_scrapper import run_scrapper
from src.configs.config import config

def main():
    url = config["wishlist_url"]
    items = run_scrapper(url)

    for i, item in enumerate(items, 1):
        print(f"{i}. {item['name']} - R$ {item['price']}")



if __name__ == "__main__":
    main()