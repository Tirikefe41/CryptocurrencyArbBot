#Cryptocurrency Arbitrage bot for interexchange trading of ER20 compatible tokens.

from exchangeslist import exchanges
from fastnumbers import fast_real
from idex.client import Client
from credentials import API
import operator
import ccxt


class Arbitrage:

	def __init__(self, percenThresh, fixedAmt, maxtrades):
		self.percenThresh = percenThresh
		self.pairs = []
		self.exchanges = {}
		self.fixedAmt = fixedAmt
		self.volumeThres = 20 # ETH Threshold for opportunity scan
		self.maxtrades = maxtrades


	def prepexchange(self):

		print("Generating common pairs across exchanges...{}\n".format(exchanges))
		paired = self.readpairs()

		for exchange in exchanges:

			if exchange == 'idex':        
				# To replace client API credentials..
				print("Generating Idex pairs...\n")
				client = Client("0xf43EFf8456302C5E918600FF2E29926feEAfDeA8", "0x69c8f3eedca06360163731ce108bebc77b05464d8fb34286a0e2924e4f0f37d1")
				self.exchanges[exchange] = client
				currencies = client.get_currencies()
				curr = []

				for key in currencies.items():
					curr.append(key[0]+'/ETH')

				paired = set(paired) & set(curr)

			else:
				ex = eval('ccxt.{}({})'.format(exchange, API[exchange]))
				self.exchanges[exchange] = ex
				ex.load_markets()
				syms = ex.symbols

				paired = set(paired) & set(syms)
		
		self.pairs = list(paired)
		print("total number of pairs generated for this combination is {}".format(len(self.pairs)))
		print("Common Pairs generated are: \n\n{}".format(self.pairs))

	def readpairs(self):
		end = '/ETH'
		return set([line.rstrip('\n')+end for line in open('ER20list.txt')])


	def scanArb(self):	

		for pair in self.pairs:
			priced = {}
			trackVol = {}
			print("Scanning...")

			for ex in exchanges: 				
				tick = self.exchanges[ex].fetch_ticker(pair)
				priced[ex] = tick['ask']
				trackVol[ex] = tick['quoteVolume']

				if priced[ex] is None:
					priced = {}
					break
					#print("Pair: {} Exchange: {} and price is {}\n".format(pair, ex, priced[ex]))

			res = self.checkOpportunity(priced, pair, trackVol)
			#print("response is {}".format(res))

			if res[0] == 1:
				print("\nPair: {} Exchange: {} and price is {}\n".format(pair, ex, priced[ex]))
				print("Arb opportunity found !! \n")
				print("Pair {} from {}: {} to {}: {} for {}%\n".format(pair, res[2], priced[res[2]], res[1], priced[res[1]], res[3]))
				print("Discounted Opportunistic Value:")
				print("Pair {} from {}: {} to {}: {} for {}%\n".format(pair, res[2], priced[res[2]], res[1], priced[res[1]], res[4]))
				print("Quote volume: {}".format(trackVol))
				print("Trading... {} from {} to {}".format(pair, res[2], res[1]))
				self.trade(res[2], res[1], pair)
			
			elif res[0] == 2:
				print("\nNone price value received from exchange")

			else:
				print("\nNo Opportunity found for {}".format(pair))


	def checkOpportunity(self, prices, _pair, dVol):

		print("Scanning for opportunities with profit margin > {}percent and Volume > {}ETH ".format(self.percenThresh, self.volumeThres))

		if prices:
			maxex = max(prices.items(), key=operator.itemgetter(1))[0]
			minex = min(prices.items(), key=operator.itemgetter(1))[0]

			maxprice = prices[maxex]
			minprice = prices[minex]

			buyqty = self.fixedAmt/minprice
			percentchg = ((maxprice - minprice)/minprice) * 100
			dispercentchg = self.discountedopportunity(maxex, minex, _pair, buyqty, maxprice)

			if dispercentchg > self.percenThresh and dVol[minex] > self.volumeThres and dVol[maxex] > self.volumeThres:
				return [1, maxex, minex, percentchg, dispercentchg]

			else: 
				return [0, maxex, minex, percentchg, dispercentchg]	
		else:
			return[2]

	# def trade(self, response, _dpair):
	# 	pass

	def discountedopportunity(self,maxex, minex, pair, bqty, sp):

		print("Discounting opportunity with fees...")

		token = pair.split('/')[0]
		maxfees = self.exchanges[maxex].fees
		minfees = self.exchanges[minex].fees

		purchase_fee = minfees['trading']['maker'] * bqty

		# if token in minfees['funding']['withdraw']:
		# 		 = minfees['funding']['withdraw'][token]
		# else:
		# 	withdraw_fee = bqty * 0.002 # Update result from percentage pattern recognition.
		if minex == 'hitbtc2':
			withdraw_fee = self.exchanges[minex].currencies[token]['fee']
		elif token in minfees['funding']['withdraw']:
			withdraw_fee = minfees['funding']['withdraw'][token]
		else:
			withdraw_fee = bqty * 0.002
 
		sqty = bqty - (purchase_fee+withdraw_fee)
		deposit_fee = 0 #to be modified to realtime
		sell_fee = maxfees['trading']['maker'] * sqty

		new_bal = (sqty - sell_fee) * sp
		change = ((new_bal - self.fixedAmt)/self.fixedAmt) * 100

		return change

	def trade(self,minex, maxex, pair):

		exchange1 = self.exchanges[minex]
		exchange2 = self.exchanges[maxex]
		sym = pair.split('/')[0]

		price1 = exchange1.fetch_ticker(pair)['ask']
		#balance1 = exchange1.fetch_balance()['free']['ETH']
		buy_amt = exchange1.amount_to_precision(pair, (self.fixedAmt/ price1)) # Tweaked amount using standard lot size
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

	def runARB(self):
		self.prepexchange()

		while True:
			print("Rescanning for new opportunities...\n")
			self.scanArb()
			print("Waiting for 5minutes before rescanning...")
			time.sleep(300)


