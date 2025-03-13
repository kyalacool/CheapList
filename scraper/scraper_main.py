from bs4 import BeautifulSoup
import requests
import datetime
from scraper.playwright_driver import get_html


class Scraper():
    def __init__(self, url):
        self.url = url
        html_content = get_html(self.url)
        soup = BeautifulSoup(html_content, 'html.parser')
        container = soup.find(class_="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-3")
        self.all_product = container.find_all('div', recursive=False)

    def get_name (self, product):
         product_name = product.find('div', class_='card-title')
         print(f'name = {product_name.text}')
         return product_name.text

    def get_price(self,product):
        product_price = product.find('span', class_='price-amount')
        print(f'price = {product_price.text}')
        return product_price.text

    def get_price_unit(self,product):
        product_unit_price = product.find('span', class_='unit-price')
        print(f'Unit price = {product_unit_price.text}')
        return product_unit_price.text

    def get_shop(selfself,product):
        product_shop = product.find('div', class_='store-name')
        print(f'Shop = {product_shop.text}')
        return product_shop.text


