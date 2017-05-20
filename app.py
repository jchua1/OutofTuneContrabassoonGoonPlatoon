from flask import Flask, render_template, request, redirect, session, url_for

#pip install oauth2client
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials

from httplib2 import Http

import json, os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def index():
    if "user" in session:
        return render_template("home.html", isLoggedIn = True)
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html", msg = "Please login to your account.")

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
    return render_template("login.html", msg = "You have successfully logged out.")

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    username = request.form["user"]
    password = request.form["pw"]
    if username == "" or password == "":
        return render_template("login.html", msg="Please enter both your username and password.")
    '''if ():#username not in database
        return render_template("login.html", msg = "Username incorrect. Please try again.")
    if ():#username right, password wrong
        return render_template("login.html", msg = "Password incorrect. Please try again.")'''
    session["user"] = username
    return redirect("/")




@app.route("/form")
def form():
    return render_template("form.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
