#Cryptocurrency Arbitrage bot for interexchange trading of ER20 compatible tokens.

from exchangeslist import exchanges
from fastnumbers import fast_real
from idex.client import Client
from credentials import API
import operator
import ccxt


class Arbitrage:

	def __init__(self):
		self.percenThresh = 1
		self.pairs = []
		self.exchanges = {}
		self.fixedAmt = 1
		self.volumeThres = 20 # ETH Threshold for opportunity scan


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
				print("No funds Available to trade with !!\n")
			
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

			if percentchg > self.percenThresh and dVol[minex] > self.volumeThres and dVol[maxex] > self.volumeThres:
				return [1, maxex, minex, percentchg, dispercentchg]

			else: 
				return [0, maxex, minex, percentchg, dispercentchg]	
		else:
			return[2]

	def trade(self, response, _dpair):
		pass

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
		if minex = 'hitbtc2':
			withdraw_fee = self.exchanges.currencies[token]['fee']
		elif token in minfees['funding']['withdraw']:
			withdraw = minfees['funding']['withdraw'][token]
		else:
			withdraw_fee = bqty * 0.002

		withdraw_fee = 
		sqty = bqty - (purchase_fee+withdraw_fee)
		deposit_fee = 0 #to be modified to realtime
		sell_fee = maxfees['trading']['maker'] * sqty

		new_bal = (sqty - sell_fee) * sp
		change = ((new_bal - self.fixedAmt)/self.fixedAmt) * 100

		return change



if __name__ =='__main__':
	bot = Arbitrage()
	bot.prepexchange()
	bot.scanArb()