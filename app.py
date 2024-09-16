
from flask import Flask, request, render_template, redirect, url_for, jsonify
from check import Stock
from pymongo import MongoClient

app = Flask(__name__)
s = Stock()

client = MongoClient('mongodb://localhost:27017/')
db = client.cropcoin  
farmers_collection = db.farmers  


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        fullname = request.form.get('fullname')
        aadhar = request.form.get('aadhar')
        username = request.form.get('username')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        company = request.form.get('org_name')  
        farmloc = request.form.get('farm_location')  
        farmsize = request.form.get('farm_size')

        farmers_collection.insert_one({
            'fullname': fullname,
            'aadhar': aadhar,
            'username': username,
            'password': password,
            'usertype': usertype,
            'company': company,
            'farm_location': farmloc,
            'farm_size': farmsize
        })
        
        return redirect(url_for('success'))
    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('index.html')


@app.route('/FinanceIndex.html')
def finance_index():
    return render_template('FinanceIndex.html', current_price=s.price, transactions=[])

@app.route('/marketLogin.html')
def market_login():
    return render_template('marketLogin.html')

@app.route('/marketplace.html')
def marketplace():
    return render_template('marketplace.html')

@app.route('/Invoice.html')
def invoice():
    return render_template('Invoice.html')

@app.route('/Equipment.html')
def equipments():
    return render_template('Equipment.html')
@app.route('/farmerLogin.html')
def farmer_login():
    return render_template('farmerLogin.html')

@app.route('/farmerDashboard.html')
def farmer_dashboard():
    return render_template('farmerDashboard.html')

@app.route('/farmerProfile.html')
def farmer_profile():
    return render_template('farmerProfile.html')

@app.route('/Fertilizers.html')
def fertilizers():
    return render_template('Fertilizers.html')

@app.route('/itemsBought.html')
def item_bought():
    return render_template('itemsBought.html')

@app.route('/Seeds.html')
def seeds():
    return render_template('Seeds.html')

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
