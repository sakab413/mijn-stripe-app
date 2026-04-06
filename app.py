import os
from flask import Flask, render_template, jsonify, request
from supabase import create_client

app = Flask(__name__)

# --- CONFIGURATIE (GEBRUIK JOUW EIGEN CODES) ---
SUPABASE_URL = "https://sbhyzbahdbjorxvvcbwm.supabase.co"
SUPABASE_KEY = "sb_publishable_bAu8zg7A9y6MyT7D8QEQng_c6mr6RLV" # Plak hier die lange code uit je screenshot
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- ROUTES VOOR JE WEBSITE ---

@app.route('/')
def index():
    # De landingspagina (je index.html moet in de map 'templates' staan)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Het dashboard waar de gebruiker zijn saldo ziet
    return render_template('dashboard.html')

@app.route('/connect-bank')
def connect_bank():
    # DIT IS DE OPLOSSING VOOR JE ERROR: De pagina om de bank te koppelen
    return render_template('connect_bank.html')

# --- API VOOR DE DATABASE (EIS VOOR CIJFER) ---

@app.route('/api/check-cashback')
def check_cashback():
    # Haalt de data op uit de Supabase tabel 'cashbacks'
    try:
        response = supabase.table("cashbacks").select("*").execute()
        if response.data:
            return jsonify({
                "status": "found",
                "shop": response.data[0]['shop_name'],
                "amount": response.data[0]['amount']
            })
    except Exception as e:
        print(f"Fout bij ophalen database: {e}")
    
    return jsonify({"status": "none"})

if __name__ == '__main__':
    app.run(debug=True)
