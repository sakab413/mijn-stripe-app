import stripe
import os
from Flask import Flask, render_template, redirect, jsonify, request

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        base_url = request.host_url.rstrip('/')
        session_type = request.form.get('type')

        if session_type == 'simulation':
            # Verander de weergave bij de aankoop
            price = 4500
            name = "EasyCashBack: Geverifieerde Transactie"
            description = "Automatische afhandeling van externe bestelling (incl. korting)"
        else:
            # Activatie fee
            price = 1000
            name = "EasyCashBack Activatie"
            description = "Koppel uw account voor automatische cashback-transacties"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['ideal', 'card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': name, 'description': description},
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
    return "<html><body style='text-align:center;padding-top:100px;font-family:sans-serif;'><h1>✅ EasyCashBack Voltooid</h1><p>De AI heeft uw transactie succesvol verwerkt.</p><a href='/'>Terug naar Dashboard</a></body></html>"

@app.route('/cancel')
def cancel():
    return "<h1>❌ Geannuleerd</h1><a href='/'>Terug naar EasyCashBack</a>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
