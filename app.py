import os
from flask import Flask, render_template, jsonify
from supabase import create_client

app = Flask(__name__)

# --- CONFIGURATIE ---
SUPABASE_URL = "https://sbhyzbahdbjorxvvcbwm.supabase.co"
SUPABASE_KEY = "sb_publishable_bAu8zg7A9y6MyT7D8QEQng_c6mr6RLV"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase connection error: {e}")

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect-bank')
def connect_bank():
    # Dit is nu de Single Page Experience (bank kiezen + inloggen in één)
    return render_template('bank_choice.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --- API VOOR BROWSER EXTENSIE & DASHBOARD ---
@app.route('/api/check-cashback')
def check_cashback():
    try:
        # Haal de nieuwste deal op uit Supabase
        response = supabase.table("cashbacks").select("*").execute()
        if response.data:
            return jsonify({
                "status": "found",
                "shop": response.data[0].get('shop_name', 'Onbekende Shop'),
                "amount": response.data[0].get('amount', '0.00')
            })
    except Exception as e:
        print(f"Database Error: {e}")
    
    return jsonify({"status": "none"})

if __name__ == '__main__':
    app.run(debug=True)
