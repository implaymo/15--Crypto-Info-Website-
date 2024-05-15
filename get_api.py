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
        self.crypto_name = []
    
        
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
            crypto_name = crypto["name"]
            crypto_current_price = '{:,.2f}'.format(crypto["quote"]["EUR"]["price"])
            crypto_market_cap ='{:,}'.format(int(crypto["quote"]["EUR"]["market_cap"]))
            self.most_value_cryptos.append((crypto_name, crypto_current_price, crypto_market_cap))

    def get_cryptos_description(self):
        self.get_crypto_name()
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
        top_10_crypto_name = ",".join(self.crypto_name)
        parameters = {
            'symbol': top_10_crypto_name,
            'skip_invalid': True,
        }
        session = Session()
        session.headers.update(self.headers)
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)  
            print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            
            
    def get_crypto_name(self):
        for crypto in self.most_value_cryptos:
            self.crypto_name.append(crypto[0].lower())
