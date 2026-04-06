import os
from flask import Flask, render_template, jsonify, redirect

app = Flask(__name__)

@app.route('/')
def index():
    # Dit is je landingspagina uit AI Studio
    return render_template('index.html')

@app.route('/connect-bank')
def connect_bank():
    # Stuurt de gebruiker naar het mooie bank-keuzemenu
    return render_template('bank_choice.html')

@app.route('/bank-login/<bank_name>')
def bank_login(bank_name):
    # Opent het inlogscherm voor de gekozen bank
    return render_template('bank_login_sim.html', bank=bank_name)

@app.route('/dashboard')
def dashboard():
    # Het eindstation: laat zien dat het gelukt is
    return render_template('dashboard.html', success=True)

@app.route('/api/check-cashback')
def check_cashback():
    """DEZE ROUTE IS CRUCIAAL: Hier praat je extensie mee"""
    return jsonify({
        "status": "found",
        "deals": [
            {"shop": "NIKE", "purchase_amount": 120.00, "cashback": 12.00},
            {"shop": "BOL.COM", "purchase_amount": 50.00, "cashback": 2.50}
        ]
    })

if __name__ == '__main__':
    # Zorgt dat Render de app kan starten op de juiste poort
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
