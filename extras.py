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

def Transfer(amt, token, fromex, toex):
	exchange1 = exchanges[fromex]
	exchange2 = exchanges[toex]

	if fromex == 'hitbtc2':
		order1 = exchange1.private_post_account_transfer({'currency': token, 'amount': amt, 'type': 'exchangeToBank'})
		address = exchange2.fetchDepositAddress(token)['address']
		withdrawal = exchange1.withdraw(token,amt,address)
	else:
		address = exchange2.fetchDepositAddress(token)['address']
		withdrawal = exchange1.withdraw(token,amt,address)

def readpairs():
	end = '/ETH'
	return set([line.rstrip('\n')+end for line in open('ER20list.txt')])

def Vol_Avg(exlist):

	avgVol = {}
	_ex = {}
	pairs = readpairs()

	for ex in exlist:	
		_ex[ex] = eval('ccxt.{}({})'.format(ex, API[ex]))
		_ex[ex].load_markets()
		syms = _ex[ex].symbols
		pairs = set(pairs) & set(syms)
	
	commonPairs = list(pairs)
	

	for exch in exlist:
		totVol = 0
		for p in commonPairs:
			qVol = _ex[exch].fetch_ticker(p)['quoteVolume']
			totVol = qVol + totVol
		avgVol[exch] = totVol/len(commonPairs)

	print(avgVol)



if __name__ == '__main__':
	#reverseTrade('GNT', 'hitbtc2', 1900)
	#trackOpen('DENT', 'binance')
	#cancelOrder('DENT','binance',4821926)
	#Transfer(1, 'ETH', 'hitbtc2', 'binance')
	Vol_Avg(['binance', 'hitbtc2'])