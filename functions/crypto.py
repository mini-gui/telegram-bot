#!/usr/bin/python3

# crypto.py - the module allows access to the market data available on coinmarketcap.com


import json
import requests
from datetime import datetime


def pretty_print(symbol, price, change_1d, change_7d):
    """Formats the padding of the returned message"""
    # add the heading
    grid = '{:5} {:>8.3f} > {:>6.2f} {:>6.2f}\n'.format(symbol, float(price), float(change_1d), float(change_7d))

    return grid


def get_response(num_result=5, curr="EUR"):
    """Fetch the data to feed to the bot with the latest listings for cryptos on coinmarketcap.com"""

    # the message that will be sent by the bot
    coin_message = "```\n"

    api_url = "https://api.coinmarketcap.com/v1/ticker/?convert={}&limit={}".format(curr, num_result)

    date = datetime.now().strftime("%d-%m-%y @ %H:%M")
    coin_message += 'Fetched on {}\n'.format(date)
    coin_message += 'SYMBOL PRICE(€)   1d(%)  7d(%)\n'
    res = requests.get(api_url)
    if res.ok:
        price_data = json.loads(res.text)
    else:
        res.raise_for_status()

    # parse the json for data
    for coin in price_data:
        round_price = str(round(float(coin['price_eur']), 3))
        coin_message += pretty_print(coin['symbol'], round_price, coin['percent_change_24h'], coin['percent_change_7d'])

    coin_message += '```'
    return coin_message

if __name__ == "__main__":
    user_input = int(input("Select how many results you want to show\n>> "))
    print(get_response(user_input)[4:-3])
