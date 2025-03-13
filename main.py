from scraper.database import DB_Manager
import datetime
import os
from scraper.scraper_main import Scraper

TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
ALL_MAINTYPE = {'egg': os.environ.get('EGG_URL'), 'milk_2_8' : os.environ.get('MILK_2_8_URL'), 'cheese':os.environ.get('CHEESE_URL'), 'chicken_meat' : os.environ.get('CHICKEN_MEAT_URL')}
db = DB_Manager()
date = TODAY

for k,v in ALL_MAINTYPE.items():
    db.setup()
    if db.add_it(date,k):
        sc = Scraper(url=v)
        for i in sc.all_product:
            name = sc.get_name(product=i)
            price = sc.get_price(product=i)
            price_unit = sc.get_price_unit(product=i)
            shop = sc.get_shop(product=i).lower()
            db.product_create_and_add(maintype=k, name=name, price=price,price_unit=price_unit, shop = shop, date=date)
    else :
        print('Today is already scrapped')




#TODO!!! ... WEBPAGE ...




