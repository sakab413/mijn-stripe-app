import stripe
import os
from flask import Flask, render_template, redirect, jsonify, request

# Haal de Stripe key uit de Environment Variables van Render
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        base_url = request.host_url.rstrip('/')
        # We kijken hier welk formulier is verstuurd ('setup' of 'simulation')
        session_type = request.form.get('type')

        if session_type == 'simulation':
            # Bedrag met AI korting voor de demo
            price = 4500  # €45,00
            name = "Automatische AI Transactie"
            description = "Inclusief €5,00 korting gedetecteerd door AI"
        else:
            # Normale prijs voor de eerste koppeling
            price = 5000  # €50,00
            name = "Bankkoppeling Verificatie"
            description = "Standaard bedrag voor eerste koppeling"

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
    <div style="font-family:sans-serif; text-align:center; margin-top:50px;">
        <h1>✅ Transactie Voltooid!</h1>
        <p>De betaling is succesvol verwerkt met de AI-korting.</p>
        <a href="/">Terug naar Dashboard</a>
    </div>
    """

@app.route('/cancel')
def cancel():
    return "<h1>❌ Transactie geannuleerd</h1><a href='/'>Terug</a>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
