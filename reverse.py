import ccxt


binance = ccxt.binance({'apiKey': "Nm88JciAwP32DYixVNeVukJHMR3GMUgybl77RdWU4RmHVj12KCqaKPFhp0hZWYkq",
						'secret':"aNCUlhnHx7u5cUl1sdd4CPszE1r8uj0ysogiQuM8Op815TZJRMniVKrJH99KUMvF"})

hitbtc2 =  ccxt.hitbtc2({'apiKey': "a3a4924e6480f1c24ca5a255e3a1a4d6",
						'secret':"7a49c7c5d5847d2f1c61f896a2053145"})

exchanges = {'binance':binance, 'hitbtc2': hitbtc2}

def reverseTrade(sym, ex):
	pair = '{}/ETH'.format(sym)
	exchange = exchanges[ex]
	amt = exchange.fetch_balance()['free']['sym']
	price = exchange.fetch_ticker(pair)['ask']
	buy_amt = exchange.amount_to_precision(pair, (amt/ price))
	order = exchange.create_order(pair, 'limit', 'sell',buy_amt, price)
	print('reversal order placed !')


if __name__ == '__main__':
	reverseTrade('DENT', 'binance')