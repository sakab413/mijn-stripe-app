import os
from flask import Flask, render_template, jsonify
from supabase import create_client

app = Flask(__name__)

# JOUW UNIEKE GEGEVENS
SUPABASE_URL = "https://sbhyzbahdbjorxvvcbwm.supabase.co"
SUPABASE_KEY = "sb_publishable_bAu8zg7A9y6MyT7D8QEQng_c6mr6RLV" # De key uit je screenshot

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/api/check-cashback')
def check_cashback():
    # Deze functie haalt de data echt uit de 'cashbacks' tabel die je hebt gemaakt
    try:
        response = supabase.table("cashbacks").select("*").execute()
        if response.data:
            # We sturen de eerste deal (bijv. Nike) naar de extensie
            return jsonify({
                "status": "found",
                "shop": response.data[0]['shop_name'],
                "amount": response.data[0]['amount']
            })
    except Exception as e:
        print(f"Error: {e}")
    
    return jsonify({"status": "none"})
