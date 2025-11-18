#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def get_html_content_selenium(url):
    driver = setup_driver()
    try:
        driver.get(url)
        time.sleep(5) 
        return driver.page_source
    finally:
        driver.quit()

def get_name_and_price(item):
    name_tag = item.select_one("a[id^='itemName_']")
    name = name_tag.text.strip() if name_tag else "N/A"
    
    price_whole = item.select_one(".a-price-whole")
    price_fraction = item.select_one(".a-price-fraction")
    
    if price_whole:
        price = f"{price_whole.text.strip()}{price_fraction.text.strip() if price_fraction else '00'}"
    else:
        price = "N/A"
    
    return name, price

def parse_wishlist(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    items = soup.select("#g-items li") or soup.select(".g-item-sortable") or soup.select("[data-item]")
    
    data = []
    for item in items:
        name, price = get_name_and_price(item)
        data.append({"name": name, "price": price})
    
    return data

def run_scrapper(url):
    print("Wishlist Scraper with Selenium is running...")
    html = get_html_content_selenium(url)

    data = parse_wishlist(html)

    return data


