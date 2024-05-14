from flask import Flask, render_template
from get_api import ApiProvider
app = Flask(__name__)

@app.route('/')
def hello():
    api = ApiProvider()
    api.get_top_10_cryptos()
    return render_template("index.html")

