from flask import Flask, render_template, request, redirect, session, url_for
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
from httplib2 import Http
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html", msg = "Please login to your account.")
#if "user" in session:
#    return render_template("home.html")

'''@app.route("/login")
def login():
    return render_template("login.html", msg = "Please login to your account")'''

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
    #session["user"] = username
    return redirect("/form") #redirect to a homepage

@app.route("/form")
def form():
    return render_template("form.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
