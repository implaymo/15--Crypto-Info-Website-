from flask import Flask, render_template
from get_api import ApiProvider
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app=app)



class CryptoInfo(db.Model):
    __tablename__ = "crypto_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    market_cap = db.Column(db.String, nullable=False)
    max_supply = db.Column(db.String, nullable=True)
    circulating_sup = db.Column(db.String, nullable=True)
    cmc_rank = db.Column(db.Integer, nullable=True)

api = ApiProvider()

@app.route('/')
def home():
    api.get_all_cryptos()
    top_10_cryptocurrencies = api.most_value_cryptos

    crypto_entries = []
    for crypto in top_10_cryptocurrencies:
        CryptoInfo(
            name = crypto[0],
            price = crypto[1],
            market_cap = crypto[2],
            max_supply = crypto[3],
            circulating_sup = crypto[4],
            cmc_rank = crypto[5]
        )
        crypto_entries.append(CryptoInfo)
    try:
            db.session.bulk_save_objects(crypto_entries)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error ocurred: {e}")
        
    return render_template("index.html", top_10_cryptocurrencies=top_10_cryptocurrencies)

@app.route('/cryptoinfo')
def crypto_info():
    return render_template("cryptoinfo.html")


if __name__ == '__main__':
    app.run(debug=True)