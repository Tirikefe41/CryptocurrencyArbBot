import ccxt
from credentials import API

exchanges = {'binance':ccxt.binance(API['binance']), 'hitbtc2': ccxt.hitbtc2(API['hitbtc2'])}

def reverseTrade(sym, ex, withdraw_amt):
	if ex == 'hitbtc2':
		pair = '{}/ETH'.format(sym)
		exchange = exchanges[ex]
		#exchange.private_post_account_transfer({'currency': sym, 'amount': withdraw_amt, 'type': 'bankToExchange'})
		amt = exchange.fetch_balance()['free'][sym]
		price = exchange.fetch_ticker(pair)['ask']
		buy_amt = exchange.amount_to_precision(pair, (amt))
		print(exchange.create_order(pair, 'limit', 'sell',buy_amt, 0.000505))
		print('reversal order placed !')

	else:
		pair = '{}/ETH'.format(sym)
		exchange = exchanges[ex]
		amt = exchange.fetch_balance()['free'][sym]
		price = exchange.fetch_ticker(pair)['ask']
		buy_amt = exchange.amount_to_precision(pair, (amt))
		print(exchange.create_order(pair, 'market', 'sell',buy_amt))
		print('reversal order placed !')

def trackOpen(sym, ex):
	pair = '{}/ETH'.format(sym)
	exchange = exchanges[ex]
	print(exchange.fetch_open_orders(pair))

def cancelOrder(sym, ex, id):
	pair = '{}/ETH'.format(sym)
	exchange = exchanges[ex]
	print(exchange.cancel_order(id, pair))



if __name__ == '__main__':
	reverseTrade('GNT', 'hitbtc2', 1900)
	#trackOpen('DENT', 'binance')
	#cancelOrder('DENT','binance',4821926)