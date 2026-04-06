import os
from flask import Flask, render_template, jsonify, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect-bank')
def connect_bank():
    # We sturen de gebruiker naar een 'nep' bank-keuzemenu dat jij hebt gemaakt
    return render_template('bank_choice.html')

@app.route('/bank-login/<bank_name>')
def bank_login(bank_name):
    # Simuleer het inloggen bij een specifieke bank
    return render_template('bank_login_sim.html', bank=bank_name)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', success=True)

@app.route('/api/check-cashback')
def check_cashback():
    # Dit is de 'motor' van je app die de extensie aanstuurt
    return jsonify({
        "deals": [
            {"shop": "NIKE", "amount": 120.00, "cashback": 12.00},
            {"shop": "BOL.COM", "amount": 50.00, "cashback": 2.50}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
