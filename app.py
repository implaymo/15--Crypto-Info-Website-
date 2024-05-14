from flask import Flask, render_template
from get_api import ApiProvider
app = Flask(__name__)

@app.route('/')
def home():
    api = ApiProvider()
    api.get_all_cryptos()
    print(api.most_value_cryptos)
    return render_template("index.html")

