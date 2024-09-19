from flask import Flask, request, render_template, redirect, url_for, jsonify
from check import Stock
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
s = Stock()

app.secret_key = 'your_secret_key'  # Change this to a real secret key for session management

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


client = MongoClient('mongodb://localhost:27017/')
db = client['CropCoin']
investors_collection = db['investors']
farmers_collection = db['farmers']
companies_collection = db['companies']


class User(UserMixin):
    def __init__(self, username, user_type):
        self.id = username
        self.user_type = user_type  # Store additional information if needed

@login_manager.user_loader
def load_user(username):
    user = farmers_collection.find_one({'farmerusername': username}) or \
           investors_collection.find_one({'username': username}) or \
           companies_collection.find_one({'username': username})
    
    if user:
        return User(username, user.get('usertype', 'unknown'))  # Pass additional info if needed
    return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        usertype = request.form.get('usertype')
        print(f"Received Usertype: {usertype}")

        for key, value in request.form.items():
            print(f"Form Data - {key}: {value}")

        user_data = {}
        collection = None

        # Determine the collection based on usertype
        if usertype == 'investor':
            # Fetch investor-specific fields (as needed)
            fullname = request.form.get('fullname')
            aadhar = request.form.get('aadhar')
            username = request.form.get('username')
            password = request.form.get('password')

            if fullname and aadhar and username and password:
                print(f"Investor Details: Fullname: {fullname}, Aadhar: {aadhar}, Username: {username}")
                hashed_password = generate_password_hash(password)

                user_data = {
                    'fullname': fullname,
                    'aadhar': aadhar,
                    'username': username,
                    'password': hashed_password,
                    'usertype': 'investor'
                }
                investors_collection.insert_one(user_data)
                return redirect(url_for('success'))
            else:
                return "Investor: Missing fields", 400

        elif usertype == 'farmer':
            # Farmer-specific fields
            fullname = request.form.get('farmername')
            aadhar = request.form.get('farmeraadhar')
            username = request.form.get('farmerusername')
            password = request.form.get('farmerpassword')
            farmloc = request.form.get('farm_location')
            farmsize = request.form.get('farm_size')

            # Ensure all required fields are filled
            if fullname and aadhar and username and password and farmloc and farmsize:
                print(f"Farmer Details: Fullname: {fullname}, Aadhar: {aadhar}, Username: {username}")
                print(f"Farm Location: {farmloc}, Farm Size: {farmsize}")
                hashed_password = generate_password_hash(password)

                user_data = {
                    'farmername': fullname,
                    'farmeraadhar': aadhar,
                    'farmerusername': username,
                    'farmerpassword': hashed_password,
                    'farm_location': farmloc,
                    'farm_size': farmsize,
                    'usertype': 'farmer'
                }
                farmers_collection.insert_one(user_data)
                return redirect(url_for('success'))
            else:
                return "Farmer: Missing fields", 400

        elif usertype == 'company':
            # Fetch company-specific fields
            company = request.form.get('org_name')
            companypassword = request.form.get('companypassword')
            companytype = request.form.get('companytype')
            seed_subcategories = request.form.getlist('seed_subcategories[]')
            equipment_subcategories = request.form.getlist('equipment_subcategories[]')

            # Debug prints
            print(f"Company Details: Company: {company}, Company Type: {companytype}")
            print(f"Seed Subcategories: {seed_subcategories}, Equipment Subcategories: {equipment_subcategories}")

            if company and companypassword and companytype:
                print(f"Company Details: Company: {company}, Company Type: {companytype}")
                print(f"Seed Subcategories: {seed_subcategories}, Equipment Subcategories: {equipment_subcategories}")
                hashed_companypassword = generate_password_hash(companypassword)

                user_data = {
                    'org_name': company,
                    'companypassword': hashed_companypassword,
                    'companytype': companytype,
                    'seed_subcategories': seed_subcategories,  # Corrected key
                    'equipment_subcategories': equipment_subcategories,  # Corrected key
                    'usertype': 'company'
                }
                companies_collection.insert_one(user_data)
                return redirect(url_for('success'))
            else:
                return "Company: Missing fields", 400

        else:
            # Handle invalid usertype
            print(f"Invalid Usertype: {usertype}")
            return redirect(url_for('index'))
        
    return render_template('register.html')


@app.route('/success')
def success():
    return render_template('index.html')

@app.route('/farmerLogin', methods=['GET','POST'])
def farmer_login():
    if request.method == 'POST':    
        username = request.form.get('username').lower()
        aadhar = request.form.get('aadhar')
        password = request.form.get('password')

        print(f"Received credentials - Username: {username}, Aadhar: {aadhar}")

        # Query to find the user with the correct field names
        user = farmers_collection.find_one({'farmerusername': username, 'farmeraadhar': aadhar})

        if user and check_password_hash(user['farmerpassword'], password):
            user_type = user.get('usertype', 'unknown')  # Default to 'unknown' if not set
            login_user(User(username, user_type))
            return redirect(url_for('farmer_dashboard'))
        else:
            return "Invalid credentials", 401
            
    return render_template('farmerLogin.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/farmerDashboard')
@login_required
def farmer_dashboard():
    return render_template('farmerDashboard.html')

@app.route('/farmerProfile')
@login_required
def farmer_profile():
    username = current_user.id
    user = farmers_collection.find_one({'farmerusername': username})  # Corrected field name
    if user:
        print(f"User found: {user}")  # Debugging line
        return render_template('farmerProfile.html', farmer=user)
    else:
        print("No user found")  # Debugging line
        return "User not found", 404

@app.route('/Fertilizers.html')
def fertilizers():
    return render_template('Fertilizers.html')

@app.route('/itemsBought.html')
def item_bought():
    return render_template('itemsBought.html')

@app.route('/Seeds.html')
def seeds():
    return render_template('Seeds.html')

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
