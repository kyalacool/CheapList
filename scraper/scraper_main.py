from bs4 import BeautifulSoup, Tag
import requests
import datetime
from scraper.playwright_driver import get_html
import re


class Scraper:
    def __init__(self, url: str):
        self.url = url
        html_content = get_html(self.url)
        soup = BeautifulSoup(html_content, 'html.parser')
        container = soup.find(class_="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-3")
        self.all_product = container.find_all('div', recursive=False)

    @staticmethod
    def get_name(product: Tag) -> str:
         product_name = product.find('div', class_='card-title')
         print(f'name = {product_name.text}')
         return product_name.text

    @staticmethod
    def get_price(product: Tag) -> int:
        product_price = product.find('span', class_='price-amount')
        raw_price = re.sub(r'\D', '', product_price.text)
        result = int(raw_price)
        print(f'price = {result}')
        return result

    @staticmethod
    def get_price_type(product: Tag) -> str:
        product_price = product.find('span', class_='price-amount')
        raw_price = product_price.text.replace('\xa0', ' ')
        result = str(raw_price.split(' ')[1])
        print(f'price_type = {result}')
        return result

    @staticmethod
    def get_price_unit(product: Tag) -> int:
        product_unit_price = product.find('span', class_='unit-price')
        result = re.sub(r'\D', '', product_unit_price.text)
        final_result = int(result)
        print(f'Unit price = {final_result}')
        return final_result

    @staticmethod
    def get_price_unit_type(product: Tag) -> str:
        product_unit_price = product.find('span', class_='unit-price')
        result = re.split(r'\d+', product_unit_price.text)[1]
        final_result = str(result)
        print(f'Unit price type : {final_result}')
        return final_result

    @staticmethod
    def get_shop(product: Tag) -> str:
        product_shop = product.find('div', class_='store-name')
        print(f'Shop = {product_shop.text}')
        return product_shop.text


