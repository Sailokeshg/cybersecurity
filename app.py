import random
import string
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from faker import Faker

app = Flask(__name__)
app.secret_key = 'secret'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cybersecurity'

def generate_random_phone():
    return ''.join(random.choice(string.digits) for _ in range(10))

fake = Faker()

db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = db.cursor(dictionary=True)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Phonenumber VARCHAR(10) NOT NULL
    )
""")

db.commit()

for i in range(1, 1001):
    name = fake.name()
    email = fake.email()
    phonenumber = generate_random_phone()
    cursor.execute("INSERT INTO customer (Name, Email, Phonenumber) VALUES (%s, %s, %s)", (name, email, phonenumber))

db.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return render_template('app.html', title='Customer Database', customers=customers)

@app.route('/addcustomer', methods=['GET', 'POST'])
def addcustomer():
    if request.method == 'POST':
        name = request.form['name']
        customer_id = request.form['id']
        email = request.form['email']
        phonenumber = request.form['phonenumber']

        cursor.execute("INSERT INTO customers (id, Name, Email, Phonenumber) VALUES (%s, %s, %s, %s)", (customer_id, name, email, phonenumber))
        db.commit()

        return redirect(url_for('index'))

    return render_template('addcustomer.html', title='Add Customer')

@app.route('/search_customer', methods=['POST'])
def search_customer():
    customer_id = request.form['search_id']
    
    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()

    if customer:
        return render_template('search_result.html', title='Search Result', customer=customer)
    else:
        return render_template('customer_not_found.html', title='Customer Not Found')

@app.route('/updatecustomer/<int:id>', methods=['GET', 'POST'])
def updatecustomer(id):
    cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
    customer = cursor.fetchone()

    if not customer:
        flash('Customer not found.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        customer['Name'] = request.form['name']
        customer['Email'] = request.form['email']
        customer['Phonenumber'] = request.form['phonenumber']

        cursor.execute("UPDATE customers SET Name = %s, Email = %s, Phonenumber = %s WHERE id = %s",
                       (customer['Name'], customer['Email'], customer['Phonenumber'], id))
        db.commit()

        
        return redirect(url_for('index'))

    return render_template('updatecustomer.html', title='Update Customer', customer=customer)

@app.route('/deletecustomer/<int:id>')
def deletecustomer(id):
    cursor.execute("DELETE FROM customers WHERE id = %s", (id,))
    db.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
