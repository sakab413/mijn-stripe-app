import stripe
import os
from flask import Flask, render_template, redirect, jsonify, request

# Haal de Stripe key uit de Environment Variables van Render
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    # Deze route laat de "stille" AI-detectie zien voor je demo
    return render_template('scan.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        base_url = request.host_url.rstrip('/')
        session_type = request.form.get('type')

        if session_type == 'simulation':
            # Bedrag met €5,- AI korting (van €50 naar €45)
            price = 4500
            name = "Automatische AI Transactie"
            description = "Gedetecteerde aankoop: €50,00 | Toegepaste korting: €5,00"
        else:
            # Jouw winst/service fee
            price = 1000
            name = "Bankkoppeling & Service Fee"
            description = "Eenmalige activatie van de AI Discount Engine"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['ideal', 'card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': name,
                        'description': description,
                    },
                    'unit_amount': price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{base_url}/success",
            cancel_url=f"{base_url}/cancel",
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def success():
    return """
    <div style="font-family:sans-serif; text-align:center; margin-top:100px;">
        <h1 style="color: #24b47e; font-size: 50px;">✅</h1>
        <h2>Transactie Geslaagd!</h2>
        <p>De AI heeft de betaling succesvol verwerkt.</p>
        <a href="/" style="color: #6772e5; text-decoration: none;
