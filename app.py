from flask import Flask, request, jsonify, render_template
from models import db, ExchangeRate
import requests
from datetime import datetime

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

API_URL = "https://open.er-api.com/v6/latest/USD"

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_rates', methods=['POST'])
def update_rates():
    response = requests.get(API_URL)
    data = response.json()

    
    if 'rates' not in data:
        return jsonify({"error": "Ошибка получения курсов"}), 500

    ExchangeRate.query.delete()

    now = datetime.utcnow()

    for currency, rate in data['rates'].items():
        db.session.add(ExchangeRate(
            base="USD", 
            currency=currency,
            rate=rate,
            updated_at=now
        ))

    db.session.commit()

    return jsonify({"message": "Курсы обновлены"})


@app.route('/last_update')
def last_update():
    rate = ExchangeRate.query.first()
    if not rate:
        return jsonify({"last_update": "нет данных"})

    return jsonify({
        "last_update": rate.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@app.route('/convert', methods=['POST'])
def convert():
    data = request.json

    from_cur = data.get('from')
    to_cur = data.get('to')
    amount = float(data.get('amount'))

    r1 = ExchangeRate.query.filter_by(currency=from_cur).first()
    r2 = ExchangeRate.query.filter_by(currency=to_cur).first()

    if not r1 or not r2:
        return jsonify({"error": "Валюта не найдена"})

    result = amount / r1.rate * r2.rate

    return jsonify({"result": round(result, 2)})


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
