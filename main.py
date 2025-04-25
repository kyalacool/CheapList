import datetime
import os
from collections import defaultdict

from flask import Flask, render_template, request
from flask_bootstrap5 import Bootstrap

from database import is_it_updated, last_update, CheapestClass, CheapestShop, DbManager
from scraper import  Scraper

TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
ALL_MAINTYPE = {'egg': os.environ.get('EGG_URL'), 'milk_2_8' : os.environ.get('MILK_2_8_URL'), 'cheese':os.environ.get('CHEESE_URL'), 'chicken_meat' : os.environ.get('CHICKEN_MEAT_URL'), 'sea_fish' : os.environ.get('SEA_FISH')}
db = DbManager()
date = TODAY

def main():
    for k,v in ALL_MAINTYPE.items():
        db.setup()
        if db.add_it(date,k):
            try :
                sc = Scraper(url=v)
                for i in sc.all_product:
                    name = sc.get_name(product=i)
                    price = sc.get_price(product=i)
                    price_type= sc.get_price_type(product= i)
                    price_unit = sc.get_price_unit(product=i)
                    price_unit_type = sc.get_price_unit_type(product=i)
                    shop = sc.get_shop(product=i).lower()
                    db.product_create_and_add(maintype=k, name=name, price=price, price_type= price_type, price_unit=price_unit, price_unit_type=price_unit_type, shop = shop, date=date)
            except AttributeError:
                print('Something wrong with the source.')
        else :
            print('Today is already scrapped')

main()

app = Flask(__name__)
Bootstrap(app)
hun_en= {'sea_fish' : 'Tengeri hal', 'chicken_meat' : 'Csirkehús', 'cheese' : 'Sajt', 'milk_2_8' : 'Tej (2,8%)', 'egg' : 'Tojás'}

@app.route('/', methods = ['GET','POST'])
def home():
    update = is_it_updated()
    last_update_result = last_update()
    return render_template('index.html', list=ALL_MAINTYPE.keys(), update=update, last_update=last_update_result, hun_en = hun_en)

@app.route('/submit', methods= ['GET', 'POST'])
def submit():
    result = request.form.getlist('selected_items')
    cheapest_product_result = {}
    for i in result :
        cc = CheapestClass(i)
        cheapest_product_result[i] = {'price_unit' : cc.myprice, 'unit_type' : cc.myunit, 'shop_and_product' : cc.shop_and_product}
    cheapest_shop_list = []
    for i in result :
        cs = CheapestShop(i)
        cheapest_shop_list.append(cs.cheapest_price)
    cheapest_shop_result = defaultdict(int)
    for d in cheapest_shop_list:
        for key, value in d.items():
            cheapest_shop_result[key] += value
    cheapest_shop_result = dict(sorted(cheapest_shop_result.items(), key= lambda item:item[1]))
    print(cheapest_shop_result)
    return render_template('submit.html', result = result, cheapest_product_result = cheapest_product_result, cheapest_shop_result= cheapest_shop_result, today = TODAY, hun_en= hun_en)


if __name__ == '__main__':
    app.run(debug= True, host='0.0.0.0',port='5005')





