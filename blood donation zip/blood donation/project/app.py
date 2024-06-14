from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'database': 'donors_db'
}

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the donor registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        donor = {
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'blood_type': request.form['blood-type'],
            'city': request.form['city'],
            'phone': request.form['phone']
        }

        # Insert donor into the MySQL database
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            query = ("INSERT INTO donors "
                     "(name, age, gender, blood_type, city, phone) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            data = (donor['name'], donor['age'], donor['gender'], donor['blood_type'], donor['city'], donor['phone'])
            cursor.execute(query, data)
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "Database connection failed."

        return redirect(url_for('donors'))
    return render_template('register.html')

# Route for the list of donors
@app.route('/donors')
def donors():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donors")
        donor_list = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('donors.html', donors=donor_list)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Database connection failed."

if __name__ == '__main__':
    app.run(debug=True, port=5001)
