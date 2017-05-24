from flask import Flask, render_template, request, redirect, session, url_for

#pip install oauth2client
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials

from httplib2 import Http

from utils.db_manager import *

import json, os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def index():
    if "admin" in session:
        return render_template("home.html", isLoggedIn = True, isAdmin = True)
    if "teacher" in session:
        return render_template("home.html", isLoggedIn = True, isAdmin = False)
    return render_template("home.html")

@app.route("/logout")
def logout():
    if "teacher" in session:
        session.pop("teacher")
    if "admin" in session:
        session.pop("admin")
    #session.pop('credentials')
    return render_template("home.html", msg = "You have successfully logged out.")

@app.route("/login")
def oauth_testing():
    flow = flow_from_clientsecrets('client_secrets.json',
                                   scope = 'https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri = url_for('oauth_testing', _external = True))
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('sample_info_route'))

@app.route('/auth', methods = ['GET', 'POST'])
def sample_info_route():
    if 'credentials' not in session:
        return redirect(url_for('oauth_testing'))

    credentials = OAuth2Credentials.from_json(session['credentials'])
    
    if credentials.access_token_expired:
        return redirect(url_for('oauth_testing'))
    else:
        http_auth = credentials.authorize(Http())
        response, content = http_auth.request('https://www.googleapis.com/oauth2/v1/userinfo?alt=json')
        c = json.loads(content)
        #if c['email'][
        if isAdmin(c['email']):
            session['admin'] = c['email']
        else:
            #important, check in database if teacher in there
            if tExists(c['email']):
                session['teacher'] = c['email']
            else:
                return redirect("/")
        return redirect("/")

@app.route("/form")
def form():
    if 'admin' in session or 'teacher' in session:
        return render_template("form.html")
    else:
        redirect("/")

@app.route("/results")
def results():
    if 'admin' in session or 'teacher' in session:
        return render_template("results.html")
    else:
        redirect("/")

if __name__ == '__main__':
    app.debug = True
    app.run()
