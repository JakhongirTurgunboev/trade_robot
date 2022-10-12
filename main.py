import MetaTrader5 as mt5
import json
import pandas as pd
import numpy as np
import datetime as dt
import time
import datetime
from test import countdown
from buy import buy_in, buy_close
from sell import sell_in, sell_close
from sell_stop import sell_stop_close, sell_stop_in
from buy_stop import buy_stop_close, buy_stop_in

with open("credentials.json") as credentials_json:
    credentials = json.load(credentials_json)

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# display data on MetaTrader 5 version
print(mt5.version())
# connect to the trade account without specifying a password and a server
account = credentials['account']
authorized = mt5.login(account)  # the terminal database password is applied if connection data is set to be remembered
if authorized:
    print("connected to account #{}".format(account))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# now connect to another trading account specifying the password
authorized = mt5.login(login=account, server=credentials['server'], password=credentials['password'])
if authorized:
    # display trading account data 'as is'
    print(mt5.account_info())
    # display trading account data in the form of a list
    print("Show account_info()._asdict():")
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

terminal_info = mt5.terminal_info()
if terminal_info is not None:
    # display the terminal data 'as is'
    print(terminal_info)
    # display data in the form of a list
    print("Show terminal_info()._asdict():")
    terminal_info_dict = mt5.terminal_info()._asdict()
    for prop in terminal_info_dict:
        print("  {}={}".format(prop, terminal_info_dict[prop]))
    print()
   # convert the dictionary into DataFrame and print
    df = pd.DataFrame(list(terminal_info_dict.items()), columns=['property', 'value'])
    print("terminal_info() as dataframe:")
    print(df)

account_currency = mt5.account_info().currency
print("Account currency:", account_currency)


# prepare the buy request structure
symbol = input("Enter valid pair to be traded: ")
lot = float(input("Enter float number as a lot size: "))
number_of_orders = int(input("Enter number of orders: "))

utc_now = datetime.datetime.utcnow()
seconds_now = (60 * 60 * utc_now.hour) + (60 * utc_now.minute) + utc_now.second

#utc ny is 13:30
utc_ny = (13 * 60 + 30) * 60

t = utc_ny - seconds_now

# Below code start counter
countdown(t)

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# get 10 symbool M30 bars from the current day
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M30, 0, 3)

# display each element of obtained data in a new line
#print("Display obtained data 'as is'")
#for rate in rates:
#    print(rate)

# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the datetime format
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
# display data
print("\nDisplay dataframe with data")
print(rates_frame)

print(rates_frame.iloc[-2])
last_item = rates_frame.iloc[-2]

high_point = last_item['high']
low_point = last_item['low']

buy_stop_list = []
sell_stop_list = []
for i in range(0, number_of_orders):
    result_buy_stop = buy_stop_in(symbol=symbol, lot=lot, price=high_point, magic=i)
    buy_stop_list.append(result_buy_stop)
for i in range(number_of_orders, 2*number_of_orders):
    result_sell_stop = sell_stop_in(symbol=symbol, lot=lot, price=low_point, magic=i)
    sell_stop_list.append(result_sell_stop)

print(f'High:{high_point}, Low:{low_point}')

current_ask = mt5.symbol_info_tick(symbol).ask  # used for buy
current_bid = mt5.symbol_info_tick(symbol).bid  # used to sell

while True:
    time.sleep(1)
    current_ask = mt5.symbol_info_tick(symbol).ask  # used for buy
    current_bid = mt5.symbol_info_tick(symbol).bid  # used to sell
    if current_ask >= high_point:
        for i in range(0, number_of_orders):
            order = sell_stop_list[i]
            request1 = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": order['order'],
            }
            print(mt5.order_check(request1))
            mt5.order_send(request1)
        print("Current ask break")
        rate = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M30, 0, 2)
        print(rate)
        break
    if current_bid <= low_point:
        for i in range(0, number_of_orders):
            order = buy_stop_list[i]
            request1 = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": order['order'],
            }
            print(mt5.order_check(request1))
            mt5.order_send(request1)
        print("Current bid break")
        rate = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M30, 0, 2)
        print(rate)
        break

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
