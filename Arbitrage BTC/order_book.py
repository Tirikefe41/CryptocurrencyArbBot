import ccxt
from Dexchanges import exchanges, tokenlist

_exchanges = {}

def init_exchange():
		# Initialization of the exchanges.
		print("Initializing exchanges... {}".format(exchanges))

		for exchange in exchanges:
			ex = eval('ccxt.{}()'.format(exchange))
			_exchanges[exchange] = ex
			ex.load_markets()

init_exchange()

for ex in exchanges:
	for token in tokenlist:
		orderbook = _exchanges[ex].fetch_order_book (token, 5)
		print("Order book for {} is:\n {}".format(token, orderbook))