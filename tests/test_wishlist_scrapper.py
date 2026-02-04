from bs4 import BeautifulSoup

from src.scrapper.wishlist_scrapper import get_name_and_price, parse_wishlist


def test_get_name_and_price_with_price():
    html = """
    <li>
        <a id="itemName_1">Sample Item</a>
        <span class="a-price-whole">123</span>
        <span class="a-price-fraction">45</span>
    </li>
    """
    soup = BeautifulSoup(html, "html.parser")
    item = soup.select_one("li")

    name, price = get_name_and_price(item)

    assert name == "Sample Item"
    assert price == "12345"


def test_get_name_and_price_without_price():
    html = """
    <li>
        <a id="itemName_2">No Price Item</a>
    </li>
    """
    soup = BeautifulSoup(html, "html.parser")
    item = soup.select_one("li")

    name, price = get_name_and_price(item)

    assert name == "No Price Item"
    assert price == "N/A"


def test_parse_wishlist_from_g_items():
    html = """
    <ul id="g-items">
        <li>
            <a id="itemName_3">Item A</a>
            <span class="a-price-whole">50</span>
            <span class="a-price-fraction">99</span>
        </li>
        <li>
            <a id="itemName_4">Item B</a>
            <span class="a-price-whole">20</span>
        </li>
    </ul>
    """

    items = parse_wishlist(html)

    assert items == [
        {"name": "Item A", "price": "5099"},
        {"name": "Item B", "price": "2000"},
    ]


def test_parse_wishlist_from_data_item_fallback():
    html = """
    <div data-item>
        <a id="itemName_5">Fallback Item</a>
        <span class="a-price-whole">10</span>
        <span class="a-price-fraction">00</span>
    </div>
    """

    items = parse_wishlist(html)

    assert items == [{"name": "Fallback Item", "price": "1000"}]
