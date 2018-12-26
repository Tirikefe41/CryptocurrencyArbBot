import ccxt
import os.path
import time
import threading
import json

class ArbitrageUI():
    def __init__(self):
        self.allinfo = {}
        self.pairs = {}
        begin = time.time()

        start = time.time()
        print(start)
        self.GetExchanges()

        print("Time for initializing exchanges = {}\n".format(str(time.time() - start)))
        start = time.time()

        state = ""
        if os.path.isfile('altcoins.txt'):
            with open('altcoins.txt', 'r') as f:
                data = f.readlines()
                for datum in data:
                    self.pairs[datum.split('\t')[0]] = datum.split('\t')[1:]
            state = "read", "from"
        else:
            with open('altcoins.txt', 'w') as f:
                for exch in self.exchanges:
                    self.pairs[exch] = self.exchanges[exch].symbols
                    f.write('{}\t{}\n'.format(exch, '\t'.join(self.pairs[exch])))
            state = "write", "from"

        print("Time for {} exchanges {} file = {}\n".format(state[0], state[1], str(time.time() - start)))
        start = time.time()

        #Close all threads here
        self.SearchAllCoinInfo()
        print("Found {} Coins in all accessible exchanges\n".format(len(self.allinfo)))

        print("Time for gathering info on all coins ={}\n".format(str(time.time() - start)))
        start = time.time()

        with open('data.json', 'w') as fp:
            json.dump(self.allinfo, fp)

        print("Printing out Result ...... ")
        time.sleep(3)
        for symbol in self.allinfo:
            for exch in self.allinfo[symbol]:
                print(symbol, exch)
                bid = self.allinfo[symbol][exch]['bid']
                baseVol = self.allinfo[symbol][exch]['baseVolume']
                print("Bid = {}\tBase Volume = {}\n".format(bid, baseVol))

        print("Time it takes to display = " + str(time.time() - start))

        print('TIME TO CODE TO EXECUTE FINISH = ' + str(time.time() - begin))

    def GetExchanges(self):
        self.exchanges = {}
        exchs = ccxt.exchanges
        Thread = []
        index = 1
        for exch in exchs:
            #Listing of number of exchanges
            #print("Listed number of exchanges {}".format(exch))

            t = threading.Thread(target =self.GetExchange, args = (exch,index,))
            index+=1
            t.start()
            Thread.append(t)
        for thrd in Thread:
            thrd.join()


    def GetExchange(self, exch, index):
        print('Initialize exchange ' + str(index))
        try:
            ex = eval('ccxt.{}()'.format(exch))
            ex.load_markets()
            self.exchanges[exch] = ex
        except Exception as e:
            pass
        print('Done Initializing exchange ' + str(index))

    def SearchAllCoinInfo(self):
        index = 1
        Thread = []
        for exch in self.pairs:
            t = threading.Thread(target=self.GetCoinInfo, args = (exch,index,))
            index += 1
            t.start()
            Thread.append(t)
        for thrd in Thread:
            thrd.join()

    def GetCoinInfo(self, exch, index):
        self.errors = []
        print('{} - Gathering data of all coins with exchange {}'.format(str(index), exch))
        try:
            dets = self.exchanges[exch].fetch_tickers()
            for det in dets:
                if det not in self.allinfo:
                    self.allinfo[det] = {exch: dets[det]}
                else:
                    self.allinfo[det][exch] = dets[det]
        except Exception as f:
            count = 1
            for coin in self.pairs[exch]:
                print('{} - Gathering data of {} with exchange {}'.format(str(index), coin, exch))
                try:
                    det = self.exchanges[exch].fetch_ticker(coin)
                    if coin not in self.allinfo:
                        self.allinfo[coin] = {exch: det}
                    else:
                        self.allinfo[coin][exch] = det
                except Exception as e:
                    self.errors.append('{},{} --> {}'.format(exch, coin, str(e)))
                count += 1
                print('{} - Data gathered successfully data of {} with exchange {}'.format(str(index), coin, exch))

            print('{} - Data gathered successfully for all coins with exchange {}'.format(str(index), exch))

def Main():
    arbt = ArbitrageUI()

if __name__ == '__main__':
    start = time.time()
    print('Code starts at ' + str(time.ctime(start)))
    Main()
    end = time.time()