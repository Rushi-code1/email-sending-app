from flask import Flask, render_template, request, redirect, session
import smtplib
import ssl
import os
import mysql.connector
from email.message import EmailMessage


app = Flask(__name__)

app.secret_key = os.urandom(24)
conn = mysql.connector.connect(
    host='localhost', user="root", password="", database="login")
cursor = conn.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


email23 = []


@app.route("/home")
def home():
    if 'users_id' in session:
        return render_template("home.html")
    else:
        return redirect('/')


@app.route("/login_validation", methods=['POST', 'Get'])
def login_validation():
    email = request.form.get("Email")
    email23.append(email)
    password = request.form.get("Password")
    cursor.execute(
        f"""SELECT * FROM `users` WHERE `email` LIKE '{email}' AND `password`LIKE '{password}'""")
    users = cursor.fetchall()
    if len(users) > 0:
        session['users_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect("/register")


@app.route("/add_user", methods=['POST', "GET"])
def add_user():
    name = request.form.get("Name")
    email = request.form.get("Email")
    password = request.form.get("Password")
    App_specific = request.form.get("spass")
    cursor.execute(f"""SELECT * FROM `users` WHERE `email` LIKE '{email}'""")
    users = cursor.fetchall()
    if len(users) > 0:
        return redirect("/register")

    else:
        cursor .execute(
            f"""INSERT INTO `users`(`users_id`,`name`,`email`,`password`,`App_specific`)VALUES('','{name}','{email}','{password}','{App_specific}')""")
        conn.commit()
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop("users_id")
    return redirect("/")


@app.route("/send", methods=["POST", "GET"])
def send():
    msg = EmailMessage()
    sender = email23.pop()
    print(sender)
    msg['From'] = sender
    APP_specific = cursor.execute(
        f"""SELECT `App_specific`  FROM `users` WHERE `email` LIKE '{sender}'""")
    password = "onvckjgqdvmaxxxi"
    print(password)
    receiver = request.form.get("reciever")
    print(receiver)
    msg['To'] = receiver

    msg['Subject'] = request.form.get('subject')
    message = request.form.get("message")
    print(type(message))
    msg.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
    return redirect('/home')

if __name__ == "__main__":
    app.run(debug=True)
