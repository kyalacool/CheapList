from sqlalchemy import create_engine, result_tuple
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from datetime import datetime, timedelta
import os
import re

engine = create_engine(
    f"postgresql+psycopg2://{os.environ.get('MY_DB_NAME')}:{os.environ.get('MY_DB_CODE')}@{os.environ.get('MY_DB_ADDRESS')}/cheaplist_db")

def is_it_updated() -> bool:
    with engine.connect() as connection:
        latest_date = connection.execute(text('SELECT date FROM product ORDER BY date DESC LIMIT 1'))
        result = latest_date.scalar()
        if result == str(datetime.today().date()):
            return True
        else :
            return False

def last_update() -> str:
    with engine.connect() as connection:
        lastupdate = connection.execute(text('SELECT date FROM product ORDER BY date DESC LIMIT 1'))
        result = lastupdate.scalar()
        return result


class CheapestClass:
    def __init__(self, selected_product: str):
        self.selected_product = selected_product
        self.today = str(datetime.today().date())
        self.mytype_id = self.my_type()
        self.myprice = self.cheapest_unit_price()
        self.myunit = self.cheapest_unit_type()
        self.shop_and_product = self.get_products_by_price()

    @staticmethod
    def get_the_name_of_the_shop(x: int) -> str:
        with engine.connect() as conn:
            query = text(
                'SELECT name FROM shop WHERE id = :myid'
            )
            result = conn.execute(query, {'myid' : x}).scalar()
            return result

    def my_type(self) -> int:
        with engine.connect() as connection:
            mytype = text('SELECT id FROM type WHERE name = :myprod_param')
            result = connection.execute(mytype, {'myprod_param' : self.selected_product}).scalar()
            return result

    def cheapest_unit_price(self) -> int:
        with engine.connect() as conn:
            query = text(
                'SELECT price_unit FROM product WHERE date = :date_param AND type_id = :mytype_param ORDER BY price_unit ASC')
            result = conn.execute(query, {'date_param': last_update(), 'mytype_param': self.mytype_id}).scalar()
            return result

    def cheapest_unit_type(self) -> str:
        with engine.connect() as conn :
            query = text(
                'SELECT price_unit_type FROM product WHERE price_unit = :myprice'
            )
            result = conn.execute(query, {'myprice': self.cheapest_unit_price()}).scalar()
            return result

    def get_products_by_price(self) -> dict:
        with engine.connect() as conn:
            query = text(
                'SELECT shop_id,name FROM product WHERE price_unit = :myprice AND type_id= :mytype'
            )
            all_res = conn.execute(query, {'myprice' : self.myprice, 'mytype' : self.mytype_id}).all()
            return {
                self.get_the_name_of_the_shop(r.shop_id): r.name for r in all_res
            }

class CheapestShop(CheapestClass):
    def __init__(self, selected_product: str):
        super().__init__(selected_product)
        self.shops = self.get_all_shop()
        self.cheapest_price = self.cheapest_price()

    @staticmethod
    def get_all_shop() -> dict:
        with engine.connect() as conn:
            query = text(
                'SELECT * FROM shop'
            )
            all_res = conn.execute(query).all()
            return {r.id: r.name for r in all_res}

    def cheapest_price(self) -> dict :
        final_res={}
        for k,v in self.shops.items():
            with engine.connect() as conn:
                query = text(
                    'SELECT price, shop_id FROM product WHERE type_id = :mytype AND shop_id= :myshop AND date = :mydate ORDER BY price ASC'
                )
                allres = conn.execute(query, {"mytype" : self.mytype_id, "myshop": k, 'mydate' : self.today}).scalar()
                if allres is None:
                    allres = conn.execute(query, {"mytype": self.mytype_id, "myshop": k, 'mydate': last_update()}).scalar()
                final_res[v] = allres
        return final_res

