from flask import Flask, render_template
from api import ApiProvider
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app=app)


class CryptoInfo(db.Model):
    """Table and Row to store all cryptos"""
    __tablename__ = "crypto_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    market_cap = db.Column(db.String, nullable=False)
    max_supply = db.Column(db.String, nullable=True)
    circulating_sup = db.Column(db.String, nullable=True)
    cmc_rank = db.Column(db.Integer, nullable=True)

api = ApiProvider()

def get_db_data():
    return CryptoInfo.query.all()

def add_data_db(api_crypto_list):  
    for crypto in api_crypto_list:
        new_info = CryptoInfo(
            name = crypto[0],
            price = crypto[1],
            market_cap = crypto[2],
            max_supply = crypto[3],
            circulating_sup = crypto[4],
            cmc_rank = crypto[5]
        )
        try:
            db.session.add(new_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error ocurred: {e}")
        



@app.route('/')
def home():
    api.get_crypto_api()
    api.store_cryptos() 
    add_data_db(api.all_cryptos)   
    all_cryptos = CryptoInfo.query.all()

    return render_template("index.html", all_cryptos=all_cryptos)

@app.route('/cryptoinfo/<int:id>')
def crypto_info(id):
    return render_template("cryptoinfo.html")


if __name__ == '__main__':
    app.run(debug=True)