from Dexchanges import exchanges, tokenlist
import operator
import ccxt

class Arb:

	def __init__(self):

		self.pairs = tokenlist
		self.exchanges = {}
		self.minProfit = 0.1 #In perecentage

	def init_exchange(self):
		# Initialization of the exchanges.
		print("Initializing exchanges... {}".format(exchanges))

		for exchange in exchanges:
			ex = eval('ccxt.{}()'.format(exchange))
			self.exchanges[exchange] = ex
			ex.load_markets()

	def Scan4Arb(self):
		

		for pair in tokenlist:
			priced = {}
			for ex in exchanges:
				priced[ex] = self.exchanges[ex].fetch_ticker(pair)['bid']

			res = self.checkOpportunity(priced)

			if res[0]:
				print("Pair: {} Exchange: {} and price is {}\n".format(pair, ex, priced[ex]))
				print("Arb opportunity found !! \n")
				print("Pair {} from {}: {} to {}: {} for {}%\n".format(pair, res[2], priced[res[2]], res[1], priced[res[1]], res[3]))
			else:
				print("No Opportunity found for {}".format(pair))

	def checkOpportunity(self, prices):

		maxex = max(prices.items(), key=operator.itemgetter(1))[0]
		minex = min(prices.items(), key=operator.itemgetter(1))[0]

		maxprice = prices[maxex]
		minprice = prices[minex]

		percentchg = ((maxprice - minprice)/minprice) * 100

		if percentchg > self.minProfit:
			return [1, maxex, minex, percentchg]

		else: 
			return [0, maxex, minex, percentchg]		





if __name__ =='__main__':
	bot = Arb()
	bot.init_exchange()
	bot.Scan4Arb()


