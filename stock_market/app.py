from flask import Flask, request, render_template, redirect, url_for, jsonify
from stock import Stock
import socket

app = Flask(__name__)
stock = Stock()

@app.route('/')
def index():
    current_price = stock.update_price(stock.outstanding_shares)
    return render_template('index.html', current_price=current_price, transactions=stock.transactions)

@app.route('/buy', methods=['POST'])
def buy():
    quantity = int(request.form['quantity'])
    current_price = stock.update_price(stock.outstanding_shares)
    new_price = stock.buy(current_price, quantity)
    return redirect(url_for('index'))

@app.route('/sell', methods=['POST'])
def sell():
    quantity = int(request.form['quantity'])
    current_price = stock.update_price(stock.outstanding_shares)
    new_price = stock.sell(current_price, quantity)
    return redirect(url_for('index'))

def get_current_price():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    price = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return price

@app.route('/price')
def price():
    return jsonify({'price': get_current_price()})

if __name__ == "__main__":
    app.run(debug=True)
