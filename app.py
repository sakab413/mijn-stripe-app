import os
from flask import Flask, render_template, redirect, jsonify, request
from nordigen import NordigenClient

app = Flask(__name__)

# Haal keys uit Render Environment Variables
NORDIGEN_ID = os.environ.get('NORDIGEN_ID')
NORDIGEN_KEY = os.environ.get('NORDIGEN_KEY')

# Initialiseer de Bank API Client
client = NordigenClient(secret_id=NORDIGEN_ID, secret_key=NORDIGEN_KEY)

# Winkels waar we cashback op geven
CASHBACK_RULES = {
    "NIKE": 0.10, 
    "BOL.COM": 0.05, 
    "AMAZON": 0.05, 
    "COOLBLUE": 0.03
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/connect-bank')
def connect_bank():
    """Start de officiële bankkoppeling via GoCardless Sandbox"""
    client.generate_token()
    # Gebruik de Sandbox bank 'SANDBOXFINANCE_SFIN0000' voor de demo
    init = client.initialize_session(
        institution_id='SANDBOXFINANCE_SFIN0000',
        redirect_url=f"{request.host_url.rstrip('/')}/bank-callback",
        reference="user-unique-session-123"
    )
    return redirect(init.link)

@app.route('/bank-callback')
def bank_callback():
    """Na het inloggen bij de bank sturen we de gebruiker naar hun dashboard"""
    return redirect('/dashboard')

@app.route('/api/check-cashback')
def check_cashback():
    """API die de 'echte' transacties simuleert voor de demo"""
    mock_transactions = [
        {"vendor": "NIKE ONLINE STORE", "amount": -89.99},
        {"vendor": "BOL.COM BV", "amount": -45.00}
    ]
    
    found_deals = []
    for tx in mock_transactions:
        for shop, rate in CASHBACK_RULES.items():
            if shop in tx['vendor'].upper():
                found_deals.append({
                    "shop": shop,
                    "purchase_amount": abs(tx['amount']),
                    "cashback": round(abs(tx['amount']) * rate, 2)
                })
    
    return jsonify({"deals": found_deals})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
