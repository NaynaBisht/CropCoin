from flask import Flask, request, render_template, redirect, url_for, jsonify
from check import Stock

app = Flask(__name__)
s = Stock()

@app.route('/')
def index():
    return render_template('index.html', current_price=s.price, transactions=[])

@app.route('/buy', methods=['POST'])
def buy():
    quantity = int(request.form['quantity'])
    s.buy(quantity)
    return '', 204

@app.route('/sell', methods=['POST'])
def sell():
    quantity = int(request.form['quantity'])
    s.sell(quantity)
    return '', 204

@app.route('/transactions')
def transactions():
    # Assuming 's.transactions' contains the list of transactions
    transactions_list = s.transactions  # Replace this with actual transaction fetching logic
    return jsonify({'transactions': transactions_list})

if __name__ == "__main__":
    app.run(debug=True)
