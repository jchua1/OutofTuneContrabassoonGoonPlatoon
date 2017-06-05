import sqlite3, hashlib, random, csv
'''
DATABASE FUNCTION DIRECTORY:
isAdmin(email)
tExists(email)
editResponse(email,responses)
addTeachers()
addAdmins()
addCourses()
getCourses(email)
getPds(email)
getRooms(email)
getLunch(email)
getYears(email)
getEmail(fname,lname)
getName(email)
courseList()
deptSort(department)
whoChoseWhat(area,number,choice)
hasEntry(email)
'''


#this is going to be used in an if(teacher email): [if(matches admin) 2] [else 1] else: 0
#requires OAuth or smth
def isAdmin( email ):
    db = sqlite3.connect("data/data.db")
    users = db.cursor()
    
    q = "SELECT * FROM admins WHERE email = \"%s\";" % ( email )
    users.execute(q)
    info = users.fetchall()

    if (len(info) > 0): #check if any admin has a matching email
        return True
    return False
        
#this method takes a teacher's email and returns true if they have an entry in teachers table
def tExists( email ):
    db = sqlite3.connect("data/data.db")
    users = db.cursor()

    q = "SELECT * FROM teachers WHERE email = \"%s\";" % ( email )
    users.execute(q)
    info = users.fetchall()

    if (len(info) > 0):
        return True #teacher already exists in database
    else:
        return False #if false it should ask a teacher for their name + department, then add them to the db

#this method alters all of the teacher (corresponding to their email)'s form responses
#uses hasEntry to see if it needs to be inserted or updated
def editResponse( email, responses ):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    course1 = responses['course1']
    course2 = responses['course2']
    course3 = responses['course3']
    pds = '1-9' if responses['period'] == 'option1' else '2-10'
    room1 = responses['room1']
    room2 = responses['room2']
    room3 = responses['room3']
    lunch1 = responses['lunch1']
    lunch2 = ''#if not selected by radio button, not in responses
    lunch3 = ''
    if 'lunch2' in responses.keys():
        lunch2 = responses['lunch2']
    if 'lunch3' in responses.keys():
        lunch3 = responses['lunch3']
    years = responses['years']
    
    if hasEntry(email):
        query = 'UPDATE responses SET course1 = "%s", course2 = "%s", course3 = "%s", pds = "%s", room1 = "%s", room2 = "%s", room3 = "%s", lunch1 = "%s", lunch2 = "%s", lunch3 = "%s", years = "%s" WHERE email = "%s";' % (course1, course2, course3, pds, room1, room2, room3, lunch1, lunch2, lunch3, years, email)
    else:
        query = 'INSERT INTO responses VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (email, course1, course2, course3, pds, room1, room2, room3, lunch1, lunch2, lunch3, years)
    c.execute(query)
    db.commit()

#adds the teachers from the csv file to the database
#executed every runtime to keep updated
def addTeachers():
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    query = 'DROP TABLE IF EXISTS teachers'#refreshing the table
    c.execute(query)

    query = 'CREATE TABLE teachers (email TEXT, first TEXT, last TEXT);'
    c.execute(query)

    f = open('data/teachers.csv')
    reader = csv.DictReader(f)
    for row in reader:
        email = row['Email address']
        first = row['First name'].capitalize()#because names are exactly as input
        last = row['Last name'].capitalize()
        query = 'INSERT INTO teachers VALUES("%s", "%s", "%s");' % (email, first, last)
        c.execute(query)
    db.commit()#gotta save everything, ya feel?
    f.close()

#adds the admins from a separate csv from the teachers to the database
#basically the same as teachers except only emails are necessary for checking
def addAdmins():
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    query = 'DROP TABLE IF EXISTS admins'
    c.execute(query)

    query = 'CREATE TABLE admins (email TEXT);'
    c.execute(query)

    f = open('data/admins.csv')
    reader = csv.reader(f)
    for row in reader:
        email = row[0]
        query = 'INSERT INTO admins VALUES("%s");' % (email)
        c.execute(query)
    db.commit()
    f.close()
    
#adds the list of courses from a csv to the database
def addCourses():
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    query = 'DROP TABLE IF EXISTS courses'
    c.execute(query)

    query = 'CREATE TABLE courses (code TEXT, title TEXT);'
    c.execute(query)

    f = open('data/courses.csv')
    reader = csv.DictReader(f)
    for row in reader:
        course = row['Course']
        coursename = row['Course Title'].upper()#just in case
        query = 'INSERT INTO courses VALUES("%s", "%s");' % (course, coursename)
        c.execute(query)
    db.commit()
    f.close()

#gotta run these
addTeachers()
addAdmins()
addCourses()

#returns the courses a teacher requested
def getCourses(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT course1,course2,course3 FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    courses = c.fetchall()[0]
    
    return courses

#returns the teacher's preferred teaching day
def getPds(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT pds FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    pds = c.fetchall()[0][0]
    
    return pds

#returns all the rooms a teacher requested
def getRooms(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT room1,room2,room3 FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    rooms = c.fetchall()[0]
    
    return rooms

#returns a teacher's preferred lunch periods
def getLunch(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT lunch1,lunch2,lunch3 FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    lunches = c.fetchall()[0]
    
    return lunches
    
#returns how many years a teacher has been working
def getYears(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT years FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    years = c.fetchall()[0][0]
    
    return years

#returns the teacher's email by name
def getEmail( fname, lname ):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT email FROM teachers WHERE first = '%s' AND last = '%s';" %(fname.capitalize(), lname.capitalize())
    c.execute(q)
    email = c.fetchall()[0][0]
    
    return email

#returns the teacher's name by email
def getName( email ):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT first,last FROM teachers WHERE email = '%s';" %(email)
    c.execute(q)
    name = c.fetchall()[0]
    name = name[0] + " " + name[1]
    
    return name

#returns a list of all course codes + courses as strings
def courseList():
    list = []
    
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT * FROM courses;"
    c.execute(q)
    mess = c.fetchall()
    for item in mess:
        list.append(item[0] + " - " + item[1])
    return list

#returns a list of courses in the specified department
#department must be written exactly like dict values
def deptSort(department):
    key = {'A' : 'Art', 'E' : 'English', 'F' : 'Foreign Language', 'H' : 'History', 'K' : 'CPR', 'M' : 'Math', 'P' : 'Phys Ed', 'S' : 'Science', 'T' : 'Tech', 'U' : 'Music', 'Z' : 'Misc'}
    list = []
    for item in courseList():
        if key[item[0]] == department:
            list.append(item)
    return list
    
#whoChoseWhat( 'lunch', 1, 4 ) returns who put 4th period as their 1st choice for lunch
#can replace lunch with room or course, and 1-3 are all valid
#whoChoseWhat( 'pds', '', '1-9' ) if responses aren't ranked, number is an empty string
def whoChoseWhat( area, number, choice ):
    people = []
    number = str(number)
    choice = str(choice)
    
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT email FROM responses WHERE %s%s = '%s';" %(area, number, choice)
    c.execute(q)
    emails = c.fetchall()
    for email in emails:
        people.append(getName(email[0]))
    
    return people

#checks if a teacher has already responded
def hasEntry(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    q = 'SELECT * FROM responses WHERE email = "%s";' %(email)
    c.execute(q)

    return len(c.fetchall()) != 0
