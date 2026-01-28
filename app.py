import stripe
import os
from flask import Flask, render_template, redirect, jsonify, request

# Haal de sleutel op uit Render settings
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/checkout_preview')
def checkout_preview():
    return render_template('checkout_preview.html')

@app.route('/webshop_success')
def webshop_success():
    return render_template('nike_cart.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # We gebruiken de huidige URL van je app voor de terugweg
        base_url = request.host_url.rstrip('/')
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['ideal', 'card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': "EasyCashBack Activatie",
                        'description': "Veilige koppeling met uw bankrekening"
                    },
                    'unit_amount': 1000, 
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{base_url}/success",
            # HIER zat de verbetering: we sturen ze naar de /cancel route
            cancel_url=f"{base_url}/cancel", 
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return f"Systeem Error: {str(e)}", 400

# De route die wordt aangeroepen als de gebruiker op 'terug' klikt in Stripe
@app.route('/cancel')
def cancel():
    # Dit stuurt ze direct terug naar je lichte dashboard
    return redirect('/')

@app.route('/success')
def success():
    return "<html><body style='text-align:center;padding-top:100px;font-family:sans-serif;'><h1>✅ Koppeling Geslaagd</h1><p>Uw bank is nu verbonden.</p><a href='/'>Terug naar Dashboard</a></body></html>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
