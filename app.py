import os
from flask import Flask, render_template, redirect, jsonify
from nordigen import NordigenClient

app = Flask(__name__)

# Config: Zet deze in Render Environment Variables!
client = NordigenClient(
    secret_id=os.environ.get('NORDIGEN_ID'),
    secret_key=os.environ.get('NORDIGEN_KEY')
)

# Lijst met winkels waar je cashback op geeft
CASHBACK_SHOPS = {
    "BOL.COM": 0.05,    # 5%
    "COOLBLUE": 0.03,   # 3%
    "NIKE": 0.10,       # 10%
    "ZALANDO": 0.07     # 7%
}

@app.route('/sync-bank')
def sync_bank():
    """Haalt de echte transacties op en checkt op matches"""
    try:
        # In een echte demo gebruik je de REQUISITION_ID van de gekoppelde bank
        # Voor nu halen we de lijst op (via de Nordigen Sandbox voor je presentatie)
        account_id = os.environ.get('BANK_ACCOUNT_ID')
        transactions = client.account(account_id).get_transactions()
        
        found_cashbacks = []
        
        # Loop door alle boekingen van de bank
        for tx in transactions['booked']:
            omschrijving = tx.get('remittanceInformationUnstructured', '').upper()
            bedrag = float(tx['transactionAmount']['amount'])
            
            # Check of de winkel in onze lijst staat
            for shop, rate in CASHBACK_SHOPS.items():
                if shop in omschrijving:
                    cashback_verdiend = abs(bedrag) * rate
                    found_cashbacks.append({
                        "winkel": shop,
                        "uitgave": bedrag,
                        "cashback": round(cashback_verdiend, 2)
                    })
        
        return jsonify({
            "status": "success",
            "gevonden_deals": found_cashbacks
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Route om de bank-koppeling te starten
@app.route('/connect-bank')
def connect_bank():
    # ... (code uit vorig bericht om link naar bank te maken)
    pass
