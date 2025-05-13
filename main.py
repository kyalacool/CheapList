from collections import defaultdict

from flask import Flask, render_template, request
from flask_bootstrap5 import Bootstrap

from database import is_it_updated, last_update, CheapestClass, CheapestShop
from ex_pw_scrape import ALL_MAINTYPE, TODAY


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
    last_update_result = last_update()
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
    return render_template('submit.html', result = result, cheapest_product_result = cheapest_product_result, cheapest_shop_result= cheapest_shop_result, today = TODAY, last_update=last_update_result, hun_en= hun_en)


if __name__ == '__main__':
    app.run(debug= True, host='0.0.0.0',port='5005')





