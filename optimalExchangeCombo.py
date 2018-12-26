import ccxt
from collections import OrderedDict


exchanges ={}
def readpairs():
		end = '/ETH'
		return set([line.rstrip('\n')+end for line in open('ER20list.txt')])

def prepexchange():

		print("Generating common pairs across exchanges...{}\n".format(exchanges))
		paired = readpairs()

		for exchange in ccxt.exchanges:
			try:	
				print("Parsing exchange {}...".format(exchange))
				ex = eval('ccxt.{}()'.format(exchange))
				
				ex.load_markets()
				syms = ex.symbols
				dpaired = set(paired) & set(syms)
				exchanges[exchange] = len(dpaired)

			except Exception:
				pass

		return exchanges

if __name__ == '__main__':
	pairdic= prepexchange()
	d_sorted = OrderedDict(sorted(pairdic.items(), key=lambda x: x[1]))

	for key,value in d_sorted.items():
		print("Exchange: {} generated {} pairs".format(key, value))