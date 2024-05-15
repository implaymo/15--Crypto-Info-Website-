from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv


class ApiProvider():
    def __init__(self) -> None:
        load_dotenv()
        self.headers = {
            'Accepts': 'applications/json',
            'X-CMC_PRO_API_KEY': os.getenv('api_key'),
        }
        self.most_value_cryptos = []
        self.top_10_cryptos_names = []

    
        
    def get_all_cryptos(self):  
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '10',
            'convert': 'EUR'
        }        
        
        session = Session()
        session.headers.update(self.headers)
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)  
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        for crypto in data["data"]:
            top_10_cryptos_names = crypto["name"]
            crypto_current_price = '{:,.2f}'.format(crypto["quote"]["EUR"]["price"])
            crypto_market_cap ='{:,}'.format(int(crypto["quote"]["EUR"]["market_cap"]))
            crypto_max_supply = crypto["max_supply"]
            crypto_circulating_supply = '{:,}'.format(crypto["circulating_supply"])
            cmc_rank = crypto["cmc_rank"]
            self.most_value_cryptos.append((top_10_cryptos_names, crypto_current_price, crypto_market_cap, crypto_max_supply, crypto_circulating_supply, cmc_rank))
            