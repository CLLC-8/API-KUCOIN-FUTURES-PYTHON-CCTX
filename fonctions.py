
import ccxt
import json, config_kuc
import pandas as pd
import sys
from pprint import pprint
import math
import time




exchange = ccxt.kucoinfutures({
    'adjustForTimeDifference': True,
    "apiKey": config_kuc.API_KEY,
    "secret": config_kuc.API_SECRET,
    'password': config_kuc.PASSWORD,
})


markets = exchange.load_markets()

def get_usdt_balance():
    try:    
        acc_balance = exchange.fetch_balance()
        return acc_balance['USDT']['free']

    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

def get_new_trade_qty(price,SLPrice,Risk):

    Delta_price_pourcent = 0
    pcloss = float(Risk)
    wallet = float(get_usdt_balance())
    quantityUSDT = 0.0
    quantityContrats = 0.0

    if SLPrice < price : #long
        Delta_price_pourcent = (price - SLPrice) / (price/ 100)
    else:
        Delta_price_pourcent = (SLPrice - price) / (price / 100)

    quantityUSDT = wallet / 100 * pcloss / Delta_price_pourcent * 100
    #quantityUSDT = float(round(quantityUSDT, 2))
    quantityContrats = quantityUSDT/price

    #print(' **** get_new_trade_qty **** ')
    print('- Wallet: ',wallet, ' USDT')
    print('- % perte autorisé: ',pcloss, ' % = ',wallet / 100 * pcloss, ' USDT')
    print('- Pourcentage /SL: ',Delta_price_pourcent, ' %')
    print ('- Quantité: ' ,quantityUSDT, ' USDT')
    #print ('- Quantité: ' ,quantityContrats, ' contracts')

    return quantityContrats






def order(side, quantity, symbol):
    try:
        for i in range(0,10):
            while True:
                try:
                    params = {'leverage': 15} 
                    order =  exchange.create_order(
                        symbol=symbol, 
                        side=side, 
                        type='market', 
                        amount=quantity,
                        params=params)

                except ccxt.RateLimitExceeded as e:
                    print("an exception occured - {}".format(e))
                    print (i)
                    time.sleep(10)
                    continue

                break
    
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    print ("ORDER EXECUTED")
    return order





def closeorder(symbol):

    quantity = get_current_position_qty(symbol)
    #quantity = quantity * 1.05
    #quantity = float("{:0.0{}f}".format(quantity,get_precision(symbol)))
    print(quantity)
    if quantity > 0.0:
        side = 'SELL'
    else:
        side = 'BUY'
    quantity =  abs(quantity)
    print(side)

    print(quantity)
    try:
        for i in range(0,10):
            while True:
                try:
                    params = {'reduceOnly': True}
                    order = exchange.create_order(
                        symbol=symbol,
                        type='market',
                        side=side,
                        amount=quantity,
                        params=params)
                except ccxt.RateLimitExceeded as e:
                    print("an exception occured - {}".format(e))
                    print (i)
                    time.sleep(10)
                    continue
                    
                break

    except Exception as e:
            print("an exception occured - {}".format(e))
            return False

    print ("CLOSE ORDER EXECUTED")
    print(f"{side} - {quantity} - {symbol}")
    return order


def get_current_position_qty(symbol):
    try:        
        balance = exchange.fetchPositions (symbols = '', params = {})
        for check_balance in balance:
            if check_balance["symbol"] == symbol:
                #pprint (check_balance)
                intside = 1
                if check_balance["side"] == 'short':
                    intside = -1
                print('quantité du trade du symbole ',symbol, ' est de ',check_balance["contracts"]*intside, ' contracts de ',check_balance["contractSize"])
                return check_balance["contracts"]*intside
                 
    except Exception as e:
        print("an exception occured - {}".format(e))
        return 0

def get_contractSize(symbol):
    print('la taille du contract du symbole ',symbol, ':', exchange.market(symbol)['contractSize'])
    return exchange.market(symbol)['contractSize']

def get_precision(symbol):
    info = exchange.market(symbol)
    #pprint (info)
    prec = (int(math.log10(info['precision']['price'])))*-1
    print('price precision du symbole ',info['precision']['price'])
    print('decimal precision du symbole ',symbol, ':', prec)
    return prec


