import ccxt
import time

exchange_dict = {'binance':ccxt.binance({'apiKey': "WvMB68Y1VECVmkpak87xxUr0ioZSxO0oosyhXC2z055B0yjnq7kl4XtuUsoZsY7g",
						'secret':"iQTQ67XaLXX9UAIZgDYNMCzTHz67OfPr8ScxeHYg45ElbxjeIxXyG5tiHKS55nIv",'enableRateLimit': True,}),
							'hitbtc2':ccxt.hitbtc2({'apiKey':"a26c7c6d7391d78b8d6eb054a3a0b688", 
								'secret':"161f90c045f3e8365674f66c38334820", 'enableRateLimit': True,})}
minex = 'hitbtc2'
maxex = 'binance'


def trade(pair):

	exchange1 = exchange_dict[minex]
	exchange2 = exchange_dict[maxex]
	sym = pair.split('/')[0]

	price1 = exchange1.fetch_ticker(pair)['ask']
	balance1 = exchange1.fetch_balance()['free']['ETH']
	buy_amt = exchange1.amount_to_precision(pair, (balance1 / price1)) # Tweaked amount using standard lot size
	low_order = exchange1.create_order(pair, 'limit', 'buy',buy_amt, price1)
	print('Placed Limit order to buy {} on {}'.format(sym, minex))

	#Generate Destination address.
	
	address = exchange2.fetchDepositAddress(sym)['address']
	print("Generated deposit address as {}".format(address))

	low_order_stat = exchange1.fetch_order(low_order['id'])

	while low_order_stat['status'] != 'closed':
		low_order_stat = exchange1.fetch_order(low_order['id'])
		print("Waiting for order to fill on {}....".format(minex))
		time.sleep(5)

	print("Bought {} on {}.".format(sym, minex))

	if minex == 'hitbtc2':
		withdraw_amt = exchange1.fetch_balance()['free'][sym] - exchange1.currencies[sym]['fee']
		order1 = exchange1.private_post_account_transfer({'currency': sym, 'amount': withdraw_amt, 'type': 'exchangeToBank'})
	else:
		withdraw_amt = exchange1.fetch_balance()['free'][sym]

	# if minex == 'hitbtc2':
	# 		#exchange1.payment_post_transfer_to_main ({'amount': withdraw_amt, 'currency_code': sym,})
			

	withdrawal = exchange1.withdraw(sym,withdraw_amt,address)
	print("Withdrawal initated...")
	time.sleep(60)
	deposit_status = True

	while deposit_status:
		# confirm new symbol balance
		deposit_bal = exchange2.fetch_balance()['free'][sym]
		if deposit_bal >= (buy_amt*0.8):
			deposit_status = False
			if maxex == 'hitbtc2':
				order1 = exchange2.private_post_account_transfer({'currency': sym, 'amount': withdraw_amt, 'type': 'bankToExchange'})

		time.sleep(10)

	print('Deposit Successful !')
	print("Selling {} on the high exchange".format(sym))

	sell_price = exchange2.fetch_ticker(pair)['ask']
	sell_amt = exchange2.amount_to_precision(pair, deposit_bal)
	high_order = exchange2.create_order(pair, 'limit', 'sell',sell_amt, sell_price)
	high_order_stat = exchange2.fetch_order(high_order['id'])

	while high_order_stat['status'] != 'closed':
		high_order_stat = exchange2.fetch_order(high_order['id'])
		print("Waiting for order to fill on {}....".format(maxex))
		time.sleep(5)

	print("Print Arbitrage Transaction completed !")
	final_balance = exchange2.fetch_balance()['free']['ETH']
	gain = (final_balance - balance1)/balance1
	print("Gained {}percent ".format(gain*100))



if __name__ == '__main__':
	
	pair = 'EVX/ETH'
	trade(pair)
	
