from flask import Flask, render_template, request, redirect, session, url_for, json

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
        if hasEntry(session['admin']):
            return render_template("home.html", isLoggedIn = True, isAdmin = True, user = getName(session['admin']), submitted = True)
        return render_template("home.html", isLoggedIn = True, isAdmin = True, user = getName(session['admin']))
    
    if "teacher" in session:
        if hasEntry(session['teacher']):
            return render_template("home.html", isLoggedIn = True, isAdmin = False, user = getName(session['teacher']), submitted = True)
        return render_template("home.html", isLoggedIn = True, isAdmin = False, user = getName(session['teacher']), submitted = False)
    
    return render_template("home.html")

@app.route("/logout")
def logout():
    if "teacher" in session:
        session.pop("teacher")
        
    if "admin" in session:
        session.pop("admin")
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
        #############commented out for testing purposes
        #if c['email'][c['email'].find('@')+1:] == 'stuy.edu':
        if isAdmin(c['email']):
            session['admin'] = c['email']
        else:
            if tExists(c['email']):
                session['teacher'] = c['email']
        return redirect('/')
        #else:
            #return render_template("home.html", msg = "Only stuy.edu emails are accepted.")

@app.route("/form")
def form():
    if 'admin' in session:
        courseStuff = courseList()
        if hasEntry(session['admin']):
            user = session['admin']
            return render_template("form.html", courses = courseStuff, isAdmin = True, submitted = True, coursesPicked = getCourses(user), pds = getPds(user), rooms = getRooms(user), lunchs = getLunch(user), years = getYears(user), msg = "You have already filled out the form.  You may edit your responses and resubmit this form.")
        return render_template("form.html", courses = courseStuff, isAdmin = True, submitted = False)
    
    if 'teacher' in session:
        courseStuff = courseList()
        if hasEntry(session['teacher']):
            user = session['teacher']
            return render_template("form.html", courses = courseStuff, submitted = True, coursesPicked = getCourses(user), pds = getPds(user), rooms = getRooms(user), lunchs = getLunch(user), years = getYears(user), msg = "You have already filled out the form.  You may edit your responses and resubmit this form.")
        return render_template("form.html", courses = courseStuff, submitted = False)
    else:
        return redirect("/")

@app.route("/results")
def results():
    # REMOVE THE "or 'teacher' in session" BEFORE THE PROJECT IS DONE
    if 'admin' in session or 'teacher' in session:
        earlySched = whoChoseWhat('pds', '', '1-9')
        lateSched = whoChoseWhat('pds', '', '2-10')

        courseReq = {}
        courseNum = {}
        courseStuff = courseList()
        for course in courseStuff:
            courseNum[course] = len(whoChoseWhat('course', 1, course)) + len(whoChoseWhat('course', 2, course)) + len(whoChoseWhat('course', 3, course))
            courseReq[course] = whoChoseWhat('course', 1, course)
            c2 = whoChoseWhat('course', 2, course)
            c3 = whoChoseWhat('course', 3, course)
            for c in c2:
                courseReq[course].append(c)
            for c in c3:
                courseReq[course].append(c)
        print courseReq
        
        
        lunchReq = {}
        lunchReq['4'] = whoChoseWhat('lunch', 1, 4)
        l2 = whoChoseWhat('lunch', 2, 4)
        l3 = whoChoseWhat('lunch', 3, 4)
        for l in l2:
            lunchReq['4'].append(l)
        for l in l3:
            lunchReq['4'].append(l)

        lunchReq['5'] = whoChoseWhat('lunch', 1, 5)
        l2 = whoChoseWhat('lunch', 2, 5)
        l3 = whoChoseWhat('lunch', 3, 5)
        for l in l2:
            lunchReq['5'].append(l)
        for l in l3:
            lunchReq['5'].append(l)

        lunchReq['6'] = whoChoseWhat('lunch', 1, 6)
        l2 = whoChoseWhat('lunch', 2, 6)
        l3 = whoChoseWhat('lunch', 3, 6)
        for l in l2:
            lunchReq['6'].append(l)
        for l in l3:
            lunchReq['6'].append(l)

        lunchReq['7'] = whoChoseWhat('lunch', 1, 7)
        l2 = whoChoseWhat('lunch', 2, 7)
        l3 = whoChoseWhat('lunch', 3, 7)
        for l in l2:
            lunchReq['7'].append(l)
        for l in l3:
            lunchReq['7'].append(l)

        lunchReq['8'] = whoChoseWhat('lunch', 1, 8)
        l2 = whoChoseWhat('lunch', 2, 8)
        l3 = whoChoseWhat('lunch', 3, 8)
        for l in l2:
            lunchReq['8'].append(l)
        for l in l3:
            lunchReq['8'].append(l)

        print lunchReq
        
        return render_template('results.html', early = earlySched, late = lateSched, courseNums = courseNum, course = courseReq, lunch = lunchReq)
    else:
        return redirect("/")

#DELETE THIS LATER
@app.route('/pie')
def pie():
    return render_template("index.html")
        
@app.route('/submit', methods = ['POST'])
def submit():
    if 'teacher' in session:
        user = session['teacher']
        responses = request.form
        editResponse(user, responses)
        return render_template("home.html", msg = "Your scheduling preferences have been recorded. Your AP will be able to view all teacher preferences and assign schedules accordingly. You may log out now.", isLoggedIn = True, isAdmin = False, user = getName(session['teacher']), submitted = True)
    
    if 'admin' in session:
        user = session['admin']
        responses = request.form
        editResponse(user, responses)
        return render_template("home.html", msg = "Your scheduling preferences have been recorded. You may log out or view all teacher requests.", isLoggedIn = True, isAdmin = True, user = getName(session['admin']), submitted = True)
    return redirect("/")

@app.route('/departments', methods = ['POST'])
def deptList():
    dept = request.form['department']
    ret = deptSort(dept)
    return json.dumps(ret)

if __name__ == '__main__':
    app.debug = True
    app.run()
