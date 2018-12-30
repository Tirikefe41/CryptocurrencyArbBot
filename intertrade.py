import ccxt
import time

exchange_dict = {'binance':ccxt.binance({'apiKey': "tcHmjrGfgrAsnFHGwQrxGBlojyKp1qPseKWUGA5j0fpfoWnhSit9NXa6BAMvPf9B",
						'secret':"sescKSnXti02q1dunzH4VNggI89A88Y6iKjDqEHi92zdTK7rn4DHjm3gJ3gWsZ8L",'enableRateLimit': True,}),
							'hitbtc2':ccxt.hitbtc2({'apiKey':"a26c7c6d7391d78b8d6eb054a3a0b688", 
								'secret':"161f90c045f3e8365674f66c38334820", 'enableRateLimit': True,})}
minex = 'binance'
maxex = 'hitbtc2'


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

	#Track Opened order
	if minex == 'binance':
		low_order_stat = exchange1.fetch_order( low_order['id'], pair)
	else:
		low_order_stat = exchange1.fetch_order(low_order['id'])

	while low_order_stat['status'] != 'closed':
		if minex == 'binance':
			low_order_stat = exchange1.fetch_order( low_order['id'], pair)
		else:
			low_order_stat = exchange1.fetch_order(low_order['id'])
		print("Waiting for order to fill on {}....".format(minex))
		time.sleep(5)

	print("Bought {} on {}.".format(sym, minex))

	if minex == 'hitbtc2':
		min_bal = exchange1.fetch_balance()['free'][sym]
		withdraw_amt = min_bal - exchange1.currencies[sym]['fee']
		order1 = exchange1.private_post_account_transfer({'currency': sym, 'amount': min_bal, 'type': 'exchangeToBank'})
	else:
		withdraw_amt = exchange1.fetch_balance()['free'][sym]

	# if minex == 'hitbtc2':
	# 		#exchange1.payment_post_transfer_to_main ({'amount': withdraw_amt, 'currency_code': sym,})
			
	print("Initialing withdrawal...")
	withdrawal = exchange1.withdraw(sym,withdraw_amt,address)
	print("Withdrawal initated...")
	time.sleep(60)
	deposit_status = True

	while deposit_status:
		# confirm new symbol balance
		print("Confirming Deposit on {}".format(maxex))
		deposit_bal = exchange2.fetch_balance()['free'][sym]
		if deposit_bal >= (withdraw_amt*0.8):
			deposit_status = False
			if maxex == 'hitbtc2':
				order1 = exchange2.private_post_account_transfer({'currency': sym, 'amount': withdraw_amt, 'type': 'bankToExchange'})

		time.sleep(5)

	print('Deposit Successful !')
	print("Selling {} on the high exchange".format(sym))

	sell_price = exchange2.fetch_ticker(pair)['ask']
	sell_amt = exchange2.amount_to_precision(pair, deposit_bal)
	high_order = exchange2.create_order(pair, 'limit', 'sell',sell_amt, sell_price)

	if maxex == 'binance':
		high_order_stat = exchange2.fetch_order(high_order['id'], pair)
	else:
		high_order_stat = exchange2.fetch_order(high_order['id'])
	

	while high_order_stat['status'] != 'closed':
		if maxex == 'binance':
			high_order_stat = exchange2.fetch_order(high_order['id'], pair)
		else:
			high_order_stat = exchange2.fetch_order(high_order['id'])
		print("Waiting for order to fill on {}....".format(maxex))
		time.sleep(5)

	print("Print Arbitrage Transaction completed !")
	final_balance = exchange2.fetch_balance()['free']['ETH']
	gain = (final_balance - balance1)/balance1
	print("Gained {}percent ".format(gain*100))



if __name__ == '__main__':	
	pair = 'BNB/ETH'
	trade(pair)
	
