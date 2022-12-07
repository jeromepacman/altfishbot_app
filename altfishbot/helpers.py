import requests


def get_tendency(self):
    if self < 20:
        return str('Very bearish')
    elif self < 45:
        return str('Bearish')
    elif self < 50:
        return str('Neutral')
    elif self < 52:
        return str('Tricky')
    elif self < 80:
        return str('Bullish')
    elif self < 100:
        return str('Very bullish')
    else:
        return str('...')


def get_market_cap():
    cap = requests.get(url='https://api.coingecko.com/api/v3/global')
    fear = requests.get(url='https://api.alternative.me/fng/?limit=1')
    tendency = requests.get(
        url='https://api.cryptometer.io/trend-indicator-v3/?api_key=KLT7vnP42Bf4k55z07sA9ImHpVd2lN11s4B3854Y')
    result_1 = cap.json()
    result_2 = fear.json()
    result_3 = tendency.json()
    data = result_1["data"]
    change = data["market_cap_change_percentage_24h_usd"]
    btc = data["market_cap_percentage"]["btc"]
    eth = data["market_cap_percentage"]["eth"]
    change = round(change, 2)
    change_price = '{:,}'.format(change)
    btc = round(btc, 2)
    domi_btc = '{:,}'.format(btc)
    eth = round(eth, 2)
    domi_eth = '{:,}'.format(eth)
    data2 = result_2["data"][0]
    feeling = data2["value_classification"]
    number = data2["value"]
    data3 = result_3["data"][0]
    buy = data3["buy_pressure"]
    sell = data3["sell_pressure"]
    score = data3["trend_score"]
    buy = round(buy)
    sell = round(sell)
    score = round(score)
    score = get_tendency(score)
    total = str(
        f' 📊 <b>Total market change:</> {change_price}% <i>(last 24 hours)</>\n🪙 <b>Bitcoin dominance:</> {domi_btc}%\n🌑 <b>Ethereum dominance:</> {domi_eth}%\n'
        f'😵 <b>Fear&Greed index: </>{feeling} ({number}|100)\n\n'
        f' 〽️<b>Current market trend:</> {score} <i>(last 4 hours)</>\n🐮 <b>Buy pressure:</> {buy}%\n🐻 <b>Sell pressure:</> {sell}%')
    req_market_cap = total
    return req_market_cap