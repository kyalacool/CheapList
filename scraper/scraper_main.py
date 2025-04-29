import datetime
import os

from database import DbManager
from scraper import  Scraper

ALL_MAINTYPE = {'egg': os.environ.get('EGG_URL'), 'milk_2_8' : os.environ.get('MILK_2_8_URL'), 'cheese':os.environ.get('CHEESE_URL'), 'chicken_meat' : os.environ.get('CHICKEN_MEAT_URL'), 'sea_fish' : os.environ.get('SEA_FISH')}
db = DbManager()
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

def main():
    for k,v in ALL_MAINTYPE.items():
        db.setup()
        if db.add_it(TODAY,k):
            try :
                sc = Scraper(url=v)
                for i in sc.all_product:
                    name = sc.get_name(product=i)
                    price = sc.get_price(product=i)
                    price_type= sc.get_price_type(product= i)
                    price_unit = sc.get_price_unit(product=i)
                    price_unit_type = sc.get_price_unit_type(product=i)
                    shop = sc.get_shop(product=i).lower()
                    db.product_create_and_add(maintype=k, name=name, price=price, price_type= price_type, price_unit=price_unit, price_unit_type=price_unit_type, shop = shop, date=TODAY)
            except AttributeError:
                print('Something wrong with the source.')
        else :
            print('Today is already scrapped')


if __name__ == '__main__':
    main()