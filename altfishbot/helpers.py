def get_tendency(self):
    if self < 20:
        return str('Very bearish')
    elif self < 45:
        return str('Bearish')
    elif self < 50:
        return str('Neutral')
    elif self < 55:
        return str('Tricky')
    elif self < 80:
        return str('Bullish')
    elif self < 100:
        return str('Very bullish')
    else:
        return str('...')