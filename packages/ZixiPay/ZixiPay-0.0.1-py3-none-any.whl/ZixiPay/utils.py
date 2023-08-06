def check_currency(currency: str):
    if currency not in {'USDZ', 'EURZ', 'LTC', 'BTC', 'ETH', 'USDT'}:
        raise ValueError(f'{currency} is not supported')
