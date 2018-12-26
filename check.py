import ccxt
exchange = ccxt.binance()
exchange.load_markets()
print(exchange.markets['ETH/BTC']['info']['status'])