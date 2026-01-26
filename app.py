import stripe
import os
from flask import Flask, render_template, redirect, jsonify

# Render leest de API key uit de 'Environment Variables' die we straks instellen
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # Dit opent je index.html bestand uit de templates map
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Dit maakt de beveiligde Stripe betaalomgeving aan
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['ideal', 'card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Aankoop via App'},
                    'unit_amount': 1000, # Bedrag in centen (€10,00)
                },
                'quantity': 1,
            }],
            mode='payment',
            # Render geeft je straks een URL, vul die hieronder in bij succes/cancel
            success_url='https://jouw-site-naam.onrender.com/',
            cancel_url='https://jouw-site-naam.onrender.com/',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    # Gebruik de poort die Render toewijst of standaard 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
