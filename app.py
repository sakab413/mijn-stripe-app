import stripe
import os
from flask import Flask, render_template, redirect, jsonify, request

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/checkout_preview')
def checkout_preview():
    return render_template('checkout_preview.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        base_url = request.host_url.rstrip('/')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['ideal', 'card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': "EasyCashBack Activatie",
                        'description': "Activeer uw account voor automatische cashback-deals"
                    },
                    'unit_amount': 1000,
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
    return "<h1>✅ EasyCashBack Geactiveerd</h1><a href='/'>Terug naar Dashboard</a>"

@app.route('/cancel')
def cancel():
    return "<h1>❌ Koppeling geannuleerd</h1><a href='/'>Terug naar EasyCashBack</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
