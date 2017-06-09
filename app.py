from flask import Flask, render_template, request, redirect, session, url_for, json, stream_with_context
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
from httplib2 import Http
from utils.db_manager import *
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
import json, os, csv, cStringIO

app = Flask(__name__)
app.secret_key = os.urandom(32)

deptData = {}

@app.route("/")
def index():
    if "admin" in session:
        if isProcessed(session['admin']):
            return render_template("home.html", isLoggedIn = True, isAdmin = True, user = getName(session['admin']), processed = True)
        if hasEntry(session['admin']):
            return render_template("home.html", isLoggedIn = True, isAdmin = True, user = getName(session['admin']), submitted = True)
        return render_template("home.html", isLoggedIn = True, isAdmin = True, user = getName(session['admin']))
    
    if "teacher" in session:
        if isProcessed(session['teacher']):
            return render_template("home.html", isLoggedIn = True, isAdmin = False, user = getName(session['teacher']), processed = True)
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
        if isProcessed(session['admin']):
            return redirect("/")
        courseStuff = courseList()
        if hasEntry(session['admin']):
            user = session['admin']
            return render_template("form.html", courses = courseStuff, isAdmin = True, submitted = True, coursesPicked = getCourses(user), pds = getPds(user), rooms = getRooms(user), lunchs = getLunch(user), years = getYears(user), msg = "You have already filled out the form.  You may edit your responses and resubmit this form.")
        return render_template("form.html", courses = courseStuff, isAdmin = True, submitted = False)
    
    if 'teacher' in session:
        if isProcessed(session['teacher']):
            return redirect("/")
        courseStuff = courseList()
        if hasEntry(session['teacher']):
            user = session['teacher']
            return render_template("form.html", courses = courseStuff, submitted = True, coursesPicked = getCourses(user), pds = getPds(user), rooms = getRooms(user), lunchs = getLunch(user), years = getYears(user), msg = "You have already filled out the form.  You may edit your responses and resubmit this form.")
        return render_template("form.html", courses = courseStuff, submitted = False)
    else:
        return redirect("/")

@app.route("/results")
def results():
    if 'admin' in session:
        
        acourses = deptSort('Art')
        earlySched = whoChoseWhat('pds', '', '1-9')
        lateSched = whoChoseWhat('pds', '', '2-10')

        if isProcessed (session['admin']):
            return render_template('results.html', early = earlySched, late = lateSched, courses = acourses, isLoggedIn = True, isAdmin= True, processed = True)
        return render_template('results.html', early = earlySched, late = lateSched, courses = acourses, isLoggedIn = True, isAdmin = True)
    else:
        return redirect("/")
        
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

@app.route('/open')
def openForm():
    if 'admin' in session:
        addTeachers()
        clearResponses()
        return render_template("home.html", msg = "You have opened the form for the semester. Teachers will now be able to access the form and fill out their scheduling preferences.", isLoggedIn = True, isAdmin = True, user = getName(session['admin']))
    return redirect("/")

@app.route('/close')
def closeForm():
    if 'admin' in session:
        processAll()
        return render_template("home.html", msg = "You have closed the form for the semester. Teachers will not be able to fill out the form anymore.", isLoggedIn = True, isAdmin = True, user = getName(session['admin']), processed = True)
    return redirect("/")

@app.route('/departments', methods = ['POST'])
def deptList():
    dept = request.form['department']
    ret = deptSort(dept)
    return json.dumps(ret)

@app.route('/responses')
def responses():
    courseNum = {}
    courseStuff = courseList()
    for course in courseStuff:
        c1 = whoChoseWhat('course', 1, course)
        c2 = whoChoseWhat('course', 2, course)
        c3 = whoChoseWhat('course', 3, course)
        courseNum[course] = len(c1) + len(c2) + len(c3)
    return json.dumps(courseNum)

@app.route('/teachers', methods = ['POST'])
def teachers():
    course = request.form['course']
    teachers = []
    c1 = whoChoseWhatE('course', 1, course)
    c2 = whoChoseWhatE('course', 2, course)
    c3 = whoChoseWhatE('course', 3, course)
    for c in c1:
        name = getName(c)
        choice = '(1st Choice)'
        years = getYears(c) + ' years'
        lunch = choicesToString(getLunch(c))
        rooms = choicesToString(getRooms(c))
        e = name + ', ' + choice + ', ' + years + ', ' + lunch + ', ' + rooms
        teachers.append(e)
    for c in c2:
        name = getName(c)
        choice = '(2nd Choice)'
        years = getYears(c) + ' years'
        lunch = choicesToString(getLunch(c))
        rooms = choicesToString(getRooms(c))
        e = name + ', ' + choice + ', ' + years + ', ' + lunch + ', ' + rooms
        teachers.append(e)
    for c in c3:
        name = getName(c)
        choice = '(3rd Choice)'
        years = getYears(c) + ' years'
        lunch = choicesToString(getLunch(c))
        rooms = choicesToString(getRooms(c))
        e = name + ', ' + choice + ', ' + years + ', ' + lunch + ', ' + rooms
        teachers.append(e)
    return json.dumps(teachers)

@app.route('/deptResponses', methods=['POST'])
def deptResponses():
    dept = request.form['dept']
    courses = deptSort(dept)
    deptData.clear()

    deptData['department'] = dept
        
    for c in courses:
        c1 = whoChoseWhatE('course', 1, c)
        c2 = whoChoseWhatE('course', 2, c)
        c3 = whoChoseWhatE('course', 3, c)
        
        for e in c1:
            if e not in deptData:
                name = getName(e)
                years = getYears(e)
                cpref = getCourses(e)
                pds = getPds(e)
                lpref = getLunch(e)
                rpref = getRooms(e)
                deptData[e] = [name, years, cpref[0], cpref[1], cpref[2], pds, lpref[0], lpref[1], lpref[2], rpref[0], rpref[1], rpref[2]]
        for e in c2:
            if e not in deptData:
                name = getName(e)
                years = getYears(e)
                cpref = getCourses(e)
                pds = getPds(e)
                lpref = getLunch(e)
                rpref = getRooms(e)
                deptData[e] = [name, years, cpref[0], cpref[1], cpref[2], pds, lpref[0], lpref[1], lpref[2], rpref[0], rpref[1], rpref[2]]
        for e in c3:
            if e not in deptData:
                name = getName(e)
                years = getYears(e)
                cpref = getCourses(e)
                pds = getPds(e)
                lpref = getLunch(e)
                rpref = getRooms(e)
                deptData[e] = [name, years, cpref[0], cpref[1], cpref[2], pds, lpref[0], lpref[1], lpref[2], rpref[0], rpref[1], rpref[2]]
                
    return ''

@app.route('/csv')
def generateCSV():
    def generate():
        data = cStringIO.StringIO()
        w = csv.writer(data)
        head = ['Email', 'Name', 'Years Taught', 'Course Pref 1', 'Course Pref 2', 'Course Pref 3', 'Schedule Preference', 'Lunch Pref 1', 'Lunch Pref 2', 'Lunch Pref 3', 'Room Pref 1', 'Room Pref 2', 'Room Pref 3']
        w.writerow(head)
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
            
        for t in deptData:
            if t != 'department':
                responses = deptData[t]
                row = [t, responses[0], responses[1], responses[2], responses[3], responses[4], responses[5], responses[6], responses[7], responses[8], responses[9], responses[10], responses[11]]
                w.writerow(row)
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)
    
    f = deptData['department'].lower().replace(" ", "_") + '_responses.csv'
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename = f)

    return Response(
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )

def choicesToString(choices):
    ret = '('
    for i in range(3):
        if i == 2:
            ret += choices[i]
        else:
            ret += choices[i] + ', '
    ret += ')'
    return ret
                
if __name__ == '__main__':
    app.debug = True
    app.run()
