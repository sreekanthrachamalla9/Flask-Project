from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configuration

db_config = {
    'user': 'root',
    'password': '9676',
    'host': 'localhost',
    'database': 'users',
}

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/users')
def users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email,role) VALUES (%s, %s, %s)", (name, email, role))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('users'))
    return render_template('new_user.html')

@app.route('/users/<int:id>')
def user_detail(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('user_detail.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
