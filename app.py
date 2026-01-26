import stripe
import os
from flask import Flask, render_template, redirect, jsonify, request

# Haal de Stripe key uit de Environment Variables van Render
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # Toont je knop uit templates/index.html
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Dit pikt automatisch de URL van jouw website op (bijv. jouw-app.onrender.com)
        base_url = request.host_url.rstrip('/')
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['ideal', 'card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Bankkoppeling & Test Aankoop'},
                    'unit_amount': 1000, # €10,00
                },
                'quantity': 1,
            }],
            mode='payment',
            # Stripe stuurt de gebruiker nu naar de juiste plek op jouw site
            success_url=f"{base_url}/success",
            cancel_url=f"{base_url}/cancel",
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403

# NIEUW: Deze pagina's vangen de gebruiker op na de betaling
@app.route('/success')
def success():
    return """
    <div style="font-family:sans-serif; text-align:center; margin-top:50px;">
        <h1>✅ Betaling Geslaagd!</h1>
        <p>Je bankrekening is succesvol gekoppeld en de test-betaling is gelukt.</p>
        <p>Je kunt dit tabblad nu sluiten en teruggaan naar de AI Studio chat.</p>
    </div>
    """

@app.route('/cancel')
def cancel():
    return """
    <div style="font-family:sans-serif; text-align:center; margin-top:50px;">
        <h1>❌ Betaling Geannuleerd</h1>
        <p>Er is geen transactie uitgevoerd. Je kunt het opnieuw proberen vanuit de app.</p>
        <a href="/">Terug naar start</a>
    </div>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
