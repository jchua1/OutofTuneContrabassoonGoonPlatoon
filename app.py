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
    print session.keys()
    return render_template("home.html", msg = "<p><b>You have successfully logged out.</b></p>")

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
        #############commented out for testing purposes
        #if c['email'][c['email'].find('@')+1:] == 'stuy.edu':
        if isAdmin(c['email']):
            session['admin'] = c['email']
        else:
            if tExists(c['email']):
                session['teacher'] = c['email']
        return redirect('/')
        #else:
            #return render_template("home.html", msg = "<p>Only <b>stuy.edu</b> emails are accepted.</p>")

@app.route("/form")
def form():
    if 'admin' in session or 'teacher' in session:
        courseStuff = courseList()
        for x in range(0, len(courseStuff)):
           courseStuff[x] = "<option value =" + courseStuff[x] + ">" + courseStuff[x] + "</option>"
        return render_template("form.html", courses = courseStuff)
    else:
        return redirect("/")

@app.route("/results")
def results():
    # REMOVE THE "or 'teacher' in session" BEFORE THE PROJECT IS DONE
    if 'admin' in session or 'teacher' in session:
        '''
        i like forgot how 2d arrays work so psuedocode
        periods[2][]
        periods[0] = whoChoseWhat('pds','','1-9')
        periods[1] = whoChoseWhat('pds','','2-10')
        ^PASS periods TO JORDAN

        courses[3][]
        courses[0] = whoChoseWhat('course',1,
        uh idk how to do courses

        lunchs[4][]
        add all the 4th periods
        lunchs[0][0] = whoChoseWhat('lunch',1,4)
        lunchs[0][1] = whoChoseWhat('lunch',2,4)
        lunchs[0][2] = whoChoseWhat('lunch',3,4)

        add all the 5th periods
        lunchs[1][0] = whoChoseWhat('lunch',1,5)
        lunchs[1][1] = whoChoseWhat('lunch',2,5)
        lunchs[1][2] = whoChoseWhat('lunch',3,5)

        add all the 6th periods
        lunchs[2][0] = whoChoseWhat('lunch',1,6)
        lunchs[2][1] = whoChoseWhat('lunch',2,6)
        lunchs[2][2] = whoChoseWhat('lunch',3,6)

        add all the 7th periods
        lunchs[3][0] = whoChoseWhat('lunch',1,7)
        lunchs[3][1] = whoChoseWhat('lunch',2,7)
        lunchs[3][2] = whoChoseWhat('lunch',3,7)
        ^PASS lunchs TO JORDAN

        i assume all my passing is through jinja'''
        
        return render_template("results.html")
    else:
        return redirect("/")

@app.route('/submit', methods = ['POST'])
def submit():
    if 'teacher' in session:
        user = session['teacher']
        responses = request.form
        print 'form submitted'
        editResponse(user, responses)
    return render_template("home.html", msg = "<p><b>Your scheduling preferences have been recorded. Your AP will be able to view all teacher preferences and assign schedules accordingly. Thank you, you may log out now.</b></p>")
    

if __name__ == '__main__':
    app.debug = True
    app.run()
