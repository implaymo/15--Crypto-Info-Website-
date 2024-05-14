from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv


class ApiProvider():
    def __init__(self) -> None:
        load_dotenv()
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        self.parameters = {
            'start': '1',
            'limit': '10',
            'convert': 'EUR'
        }
        
        self.headers = {
            'Accepts': 'applications/json',
            'X-CMC_PRO_API_KEY': os.getenv('api_key'),
        }
        
        self.most_value_cryptos = []
        
    def get_all_cryptos(self):  
        session = Session()
        session.headers.update(self.headers)
        try:
            response = session.get(self.url, params=self.parameters)
            data = json.loads(response.text)  
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        for crypto in data["data"]:
            crypto_name = crypto["name"]
            crypto_current_price = '{:,.2f}'.format(crypto["quote"]["EUR"]["price"])
            crypto_market_cap ='{:,}'.format(int(crypto["quote"]["EUR"]["market_cap"]))
            self.most_value_cryptos.append((crypto_name, crypto_current_price, crypto_market_cap))
