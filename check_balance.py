import ccxt

binance = ccxt.binance({'apiKey': "Nm88JciAwP32DYixVNeVukJHMR3GMUgybl77RdWU4RmHVj12KCqaKPFhp0hZWYkq",
						'secret':"aNCUlhnHx7u5cUl1sdd4CPszE1r8uj0ysogiQuM8Op815TZJRMniVKrJH99KUMvF"})

hitbtc2 =  ccxt.hitbtc2({'apiKey': "a3a4924e6480f1c24ca5a255e3a1a4d6",
						'secret':"7a49c7c5d5847d2f1c61f896a2053145"})

print("Binance balance: {}\n Hitbtc balance: {}".format(binance.fetch_balance()['free']['ETH'], hitbtc2.fetch_balance()['free']['ETH']))


# {'apiKey': "WvMB68Y1VECVmkpak87xxUr0ioZSxO0oosyhXC2z055B0yjnq7kl4XtuUsoZsY7g",
# 						'secret':"iQTQ67XaLXX9UAIZgDYNMCzTHz67OfPr8ScxeHYg45ElbxjeIxXyG5tiHKS55nIv"}

# {'apiKey':"a26c7c6d7391d78b8d6eb054a3a0b688", 
# 							'secret':"161f90c045f3e8365674f66c38334820 "}