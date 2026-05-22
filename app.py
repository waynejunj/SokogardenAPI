from flask import *
import pymysql
from passlib.hash import pbkdf2_sha256
import os
from flask_cors import *


# create the flask app
app = Flask(__name__)

CORS(app)

# configure the storage path of product photos
os.makedirs('static/images',exist_ok=True)
app.config['UPLOAD_FOLDER'] = 'static/images/'

# Create the signup route
@app.route('/api/signup', methods = ['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']

    # connection to database
    connection = pymysql.connect(user='kaliphisher',host='mysql-kaliphisher.alwaysdata.net',password='modcom123',database='kaliphisher_sokogarden')

    # Initialize a cursor
    cursor = connection.cursor()

    # Check if an email exist in the database
    sqlc = 'select * from users where email = %s'
    datac= (email,)

    cursor.execute(sqlc,datac)

    # Check if there is an email retured
    userc = cursor.fetchone()

    if userc:
        return jsonify({"error": "User already exists!"})

    hashed_pass = pbkdf2_sha256.hash(password)
    # create the sql query 
    sql = 'insert into users(username,email,password,phone) values(%s,%s,%s,%s)'

    # prepare data to replace the placeholders in the sql query
    data = (username,email,hashed_pass,phone)

    # use cursor to execute the query with the data
    cursor.execute(sql,data)

    # Commit the changes to the database
    connection.commit()

    # close the connection
    connection.close()

    # return a response after a successful registration
    return jsonify({'success':'User registered successfully'})

# Signin route
@app.route('/api/signin', methods = ['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    # connect to database
    connection = pymysql.connect(user='kaliphisher',host='mysql-kaliphisher.alwaysdata.net',password='modcom123',database='kaliphisher_sokogarden')

    # create cursor 
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Find the user by email
    sql = 'select * from users where email = %s'
    data = (email,)

    cursor.execute(sql,data)

    user = cursor.fetchone()

    if user is None:
        return jsonify ({'error':'Wrong credentials!'})
    
    stored_pass = user['password']

    
    # compare entered password with the stored password
    if pbkdf2_sha256.verify(password,stored_pass):
        return jsonify({'success':f"Welcome back {user['username']}",'user':user})
    
    else:
        return jsonify({'error':'Invalid credentials!'})
    
# Define the add product route
@app.route('/api/addproduct',methods = ['POST'])
def addproduct():
    product_name = request.form['product_name']
    product_description = request.form ['product_description']
    product_cost = request.form ['product_cost']

    # Extract image data
    photo = request.files['photo']

    # Get the image file name
    filename = photo.filename

    # Specify where the image will be saved
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # save the photo 
    photo.save(photo_path)

    connection = pymysql.connect(user='kaliphisher',host='mysql-kaliphisher.alwaysdata.net',password='modcom123',database='kaliphisher_sokogarden')

    # cursor
    cursor = connection.cursor()

    sql = 'insert into product_details(product_name, product_description, product_cost, product_photo) values(%s,%s,%s,%s)'
    data = (product_name,product_description,product_cost,filename)

    cursor.execute(sql,data)

    connection.commit()
    connection.close()

    return jsonify({'success': 'Product added successfully'})

# create a route to get all the products from the database
@app.route('/api/getproducts', methods=['GET'])
def getproducts():
    connection = pymysql.connect(user='kaliphisher',host='mysql-kaliphisher.alwaysdata.net',password='modcom123',database='kaliphisher_sokogarden')

    # create cursor
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = 'select * from product_details'

    cursor.execute(sql)

    connection.close

    products = cursor.fetchall()

    return jsonify({'products':products})


# Mpesa payment endpoint
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        # amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
 
        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://f426-154-159-252-35.ngrok-free.app/api/mpesa_callback",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})


from flask import request, jsonify
import json

# Global DB connection (consider using a connection pool in production)
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="wayne_sokogarden"
)

@app.route('/api/mpesa_callback', methods=['POST'])
def mpesa_callback():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"ResultCode": 1, "ResultDesc": "Invalid JSON"}), 400

        print("MPESA CALLBACK RECEIVED:", json.dumps(data, indent=2))

        stk = data.get('Body', {}).get('stkCallback', {})

        merchant_request_id = stk.get('MerchantRequestID')
        checkout_request_id = stk.get('CheckoutRequestID')
        result_code = stk.get('ResultCode')
        result_desc = stk.get('ResultDesc')

        # Default values
        phone = None
        amount = None
        receipt = None
        trans_date = None

        # Extract callback metadata only if payment was successful
        if result_code == 0:
            items = stk.get('CallbackMetadata', {}).get('Item', [])
            for item in items:
                name = item.get('Name')
                value = item.get('Value')
                
                if name == 'PhoneNumber':
                    phone = value
                elif name == 'Amount':
                    amount = value
                elif name == 'MpesaReceiptNumber':
                    receipt = value
                elif name == 'TransactionDate':
                    trans_date = value

        # Insert into database
        cursor = db.cursor()
        sql = """
            INSERT INTO mpesa_payments (
                merchant_request_id,
                checkout_request_id,
                result_code,
                result_desc,
                phone_number,
                amount,
                mpesa_receipt,
                transaction_date,
                raw_response
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            merchant_request_id,
            checkout_request_id,
            result_code,
            result_desc,
            phone,
            amount,
            receipt,
            trans_date,
            json.dumps(data)  # Always save full raw response for debugging
        ))

        db.commit()
        cursor.close()

        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
        print("Callback Error:", str(e))
        # Still try to save the raw data even if something fails
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO mpesa_payments (result_code, result_desc, raw_response)
                VALUES (%s, %s, %s)
            """, (1, str(e), json.dumps(data) if 'data' in locals() else None))
            db.commit()
            cursor.close()
        except:
            pass
        return jsonify({"ResultCode": 1, "ResultDesc": "Error processing callback"}), 500

if __name__ == '__main__':
    app.run(debug= True)