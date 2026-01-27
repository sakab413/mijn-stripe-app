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
    # We vangen de URL van de webshop op via de 'ref' parameter
    shop_url = request.args.get('ref', 'de webshop')
    return render_template('scan.html', shop_url=shop_url)

@app.route('/checkout_preview')
def checkout_preview():
    return render_template('checkout_preview.html')

@app.route('/webshop_success')
def webshop_success():
    return "<html><body style='text-align:center;padding-top:100px;font-family:sans-serif;background:#f8f9fa;'><div style='display:inline-block;background:white;padding:50px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.05);'><h1 style='color:#10b981;'>🛒 Terug bij de Webshop</h1><p>De <b>EasyCashBack</b> korting is toegepast via je gekoppelde bankrekening!</p><div style='background:#eee;padding:20px;border-radius:10px;margin:20px 0;'>Nieuw totaal: <b>€45,00</b></div><button style='padding:15px 30px;background:#333;color:white;border:none;border-radius:10px;cursor:pointer;'>Nu definitief afrekenen</button><br><br><a href='/' style='color:#94a3b8;text-decoration:none;'>Terug naar Dashboard</a></div></body></html>"

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        base_url = request.host_url.rstrip('/')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['ideal', 'card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': "EasyCashBack Activatie"},
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
    return "<h1>✅ Account Geactiveerd</h1><a href='/'>Terug naar Dashboard</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
