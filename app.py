import os
from flask import Flask, render_template, jsonify, request
from supabase import create_client

app = Flask(__name__)

# --- CONFIGURATIE ---
SUPABASE_URL = "https://sbhyzbahdbjorxvvcbwm.supabase.co"
# Let op: Gebruik de Anon Key met de juiste hoofdletters (QEQng)
SUPABASE_KEY = "sb_publishable_bAu8zg7A9y6MyT7D8QEQng_c6mr6RLV"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase connectie fout: {e}")

# --- ROUTES ---

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Fout: index.html niet gevonden in de map templates. ({e})"

@app.route('/connect-bank')
def connect_bank():
    try:
        # Dit is de pagina waar je logs over struikelden
        return render_template('bank_choice.html')
    except Exception as e:
        return f"Fout: bank_choice.html niet gevonden in de map templates. ({e})"

@app.route('/bank-login-sim')
def bank_login_sim():
    try:
        return render_template('bank_login_sim.html')
    except Exception as e:
        return f"Fout: bank_login_sim.html niet gevonden. ({e})"

@app.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return f"Fout: dashboard.html niet gevonden. ({e})"

# --- API VOOR JE DATABASE ---
@app.route('/api/check-cashback')
def check_cashback():
    try:
        # We halen data op uit de tabel 'cashbacks'
        response = supabase.table("cashbacks").select("*").execute()
        if hasattr(response, 'data') and response.data:
            return jsonify({
                "status": "found",
                "shop": response.data[0].get('shop_name', 'Onbekende Shop'),
                "amount": response.data[0].get('amount', '0.00')
            })
    except Exception as e:
        print(f"API Error: {e}")
    
    return jsonify({"status": "none"})

if __name__ == '__main__':
    app.run(debug=True)
