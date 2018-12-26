from idex.client import Client
from fastnumbers import fast_real

def CheckOrderBook(client, opt, pair):
                print("Checking order book...")
                
                depth = client.get_order_book(pair)
                
                if opt == 'bids':
                        return fast_real(depth['bids'][0]['price']), fast_real(depth['bids'][1]['price'])        
                elif opt == 'asks':
                        return fast_real(depth['asks'][0]['price']), fast_real(depth['asks'][1]['price'])
                else:
                        raise Exception('Check option needs to be bids or asks')

addr = "0xf43EFf8456302C5E918600FF2E29926feEAfDeA8"
privy = "0x69c8f3eedca06360163731ce108bebc77b05464d8fb34286a0e2924e4f0f37d1"   


client = Client(addr, privy)
pair = 'ETH_SAN'
#print(CheckOrderBook(client, 'bids', pair))
orders = client.get_open_orders(pair, addr)
#depth = client.get_order_books()
print(orders)
#print(len(depth['bids']))

