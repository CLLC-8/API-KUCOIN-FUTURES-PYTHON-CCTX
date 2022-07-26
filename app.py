#pip3 install -r requirements.txt
#venv\Scripts\activate
#heroku login
#heroku git:clone -a cllcstyle 
#git add .
#git commit -am "make it better"
#git push heroku main
#heroku logs --tailfl


import ccxt
import json, config_kuc
import pandas as pd
import sys
from pprint import pprint
from cProfile import run
from sre_constants import SUCCESS
from fonctions import *
import accounts
from flask import Flask, request, jsonify, render_template, send_from_directory


print('python', sys.version)
print('CCXT Version:', ccxt.__version__)



exchange = ccxt.kucoinfutures({
'adjustForTimeDifference': True,
'enableRateLimit': True,
"apiKey": config_kuc.API_KEY,
"secret": config_kuc.API_SECRET,
'password': config_kuc.PASSWORD,
})


markets = exchange.load_markets()



app = Flask(__name__)


@app.route("/")
def welcome():
    return  render_template('index.html')


@app.route("/webhook", methods=['POST'])
def webhook():




    data=json.loads(request.data)
    
    if data['passphrase'] != config_kuc.WEBHOOK_PASSPHRASE:
        return {
            "code":"error",
            "massage":"nice try"
        }











    symbol=data['ticker']
    side=data['order_action'].upper()
    Price=float(data['order_price'])
    stopPrice=float(data['stopPrice'])
    Risk=float(data['risk'])
    quantity = float(get_new_trade_qty(Price,stopPrice,Risk))
    print('quantité en nombre de ', symbol," :", quantity)
    quantity = float(quantity/get_contractSize(symbol))
    print('quantité en nombre de contrat :', quantity)
    #quantity = float("{:0.0{}f}".format(quantity,get_precision(symbol)))
    #print('quantité en nombre de contrat avec precision :', quantity)

    if data['type'] == "ORDER":


        print('********************NEW*ORDER*****************************')
        print(f"sending order {side} - {symbol}")

        order_response = order(side,quantity,symbol)

        #print(order_response)

        if order_response :
       
            return {
                    "code":"SUCCESS",
                    "message":"order executed",
            }

        else:
            print ("ordre failed")
            return{
                "code":"error",
                "message":"order failed"
            }
        


    if data['type'] == "CLOSE":
        print('********************CLOSE*ORDER*****************************')

        order_response = closeorder(symbol)

        #print(order_response)

        if order_response :
       
            return {
                    "code":"SUCCESS",
                    "message":"order executed",
            }

        else:
            print ("ordre failed")
            return{
                "code":"error",
                "message":"order failed"
            }






#params = {'leverage': leverage} 

#order_response = exchange.create_order(symbol=symbol, type='market', side=side, amount=amount, params=params)
#pprint(order_response)

#markets = exchange.load_markets()
#positions = exchange.fetchPositions (symbols = '', params = {})
#print(positions)

#order_response = exchange.create_order(symbol=symbol, type='market', side='sell', amount=25)
#pprint(order_response)

#order_response = exchange.market('ADA/USDT:USDT')
#pprint(order_response)

#order_response = get_precision('BTC/USDT:USDT')
#pprint(order_response)

'''
    accountsdata = json.loads(accounts.accounts_str)
    for accounts_name in accountsdata["accounts"]: 
        print(accounts_name["API_KEY"])
        exchange = ccxt.kucoinfutures({
        'adjustForTimeDifference': True,
        "apiKey": accounts_name["API_KEY"],
        "secret": accounts_name["API_SECRET"],
        'password': accounts_name["PASSWORD"],
        })

        '''
