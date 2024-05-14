from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'EUR'
}
headers = {
    'Accepts': 'applications/json',
    'X-CMC_PRO_API_KEY': os.getenv('api_key'),
}


session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)