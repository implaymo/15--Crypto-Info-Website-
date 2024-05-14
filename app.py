from flask import Flask, render_template
from get_api import ApiProvider
app = Flask(__name__)

@app.route('/')
def home():
    api = ApiProvider()
    api.get_all_cryptos()
    top_10_cryptocurrencies = api.most_value_cryptos
    return render_template("index.html", top_10_cryptocurrencies=top_10_cryptocurrencies)

