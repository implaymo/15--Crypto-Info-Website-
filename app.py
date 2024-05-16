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
    percent_change_24h = db.Column(db.String, nullable=True)
    percent_change_7d = db.Column(db.String, nullable=True)
    volume_24h = db.Column(db.String, nullable=True)

api = ApiProvider()

with app.app_context():
    db.create_all()
    
def get_db_data():
    return CryptoInfo.query.all()

def update_db(api_crypto_list, data_db): 
    for crypto in api_crypto_list:
        for data in data_db:
            if crypto[0] == data.name:
                data.name = crypto[0]
                data.price = crypto[1]
                data.market_cap = crypto[2]
                data.max_supply = crypto[3]
                data.circulating_sup = crypto[4]
                data.cmc_rank = crypto[5]
                data.percent_change_24h = crypto[6]
                data.percent_change_7d = crypto[7]
                data.volume_24h = crypto[8]
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error ocurred: {e}")

        
def add_crypto_db(api_crypto_list):
    crypto_entries = []   
    for crypto in api_crypto_list:
        new_data = CryptoInfo(
                name = crypto[0],
                price = crypto[1],
                market_cap = crypto[2],
                max_supply = crypto[3],
                circulating_sup = crypto[4],
                cmc_rank = crypto[5],
                percent_change_24h = crypto[6],
                percent_change_7d = crypto[7],
                volume_24h = crypto[8]
        )
        crypto_entries.append(new_data)
    try:
        db.session.bulk_save_objects(crypto_entries)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error ocurred: {e}")

@app.route('/')
def home():
    api.api_data()
    api.store_cryptos() 
    data_db = get_db_data() 
    if not data_db:
        add_crypto_db(api.all_cryptos)
    else:
        update_db(api.all_cryptos, data_db)    
    all_cryptos = CryptoInfo.query.all()
    return render_template("index.html", all_cryptos=all_cryptos)

@app.route('/cryptoinfo/<int:id>', methods=["GET", "POST"])
def crypto_info(id):
    request_crypto = db.get_or_404(CryptoInfo, id) 
    return render_template("cryptoinfo.html", request_crypto=request_crypto)


if __name__ == '__main__':
    app.run(debug=True)