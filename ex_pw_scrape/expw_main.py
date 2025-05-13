import requests
import os

from ex_pw_scrape.scraper_brain import ALL_MAINTYPE,TODAY, db, Scraper

def main():
    db.setup()
    for k,v in ALL_MAINTYPE.items():
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
    print('Done.')

if __name__ == '__main__':
    main()