import sqlite3, hashlib, random, csv

#this is going to be used in an if(teacher email): [if(matches admin) 2] [else 1] else: 0
#requires OAuth or smth
def isAdmin( email ):
    db = sqlite3.connect("data/data.db")
    users = db.cursor()
    
    q = "SELECT * FROM admins WHERE email = \"%s\";" % ( email )
    users.execute(q)
    info = users.fetchall()

    if (len(info) > 0): #check if an admin has a matching email
        return True
    return False
        
def tExists( email ):
    db = sqlite3.connect("data/data.db")
    users = db.cursor()

    q = "SELECT * FROM teachers WHERE email = \"%s\";" % ( email )
    users.execute(q)
    info = users.fetchall()

    print info

    if (len(info) > 0):
        return True #teacher already exists in database
    else:
        return False #if false it should ask a teacher for their name + department, then add them to the db

def editResponse( iden, responses ):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    course1 = responses['course1']
    course2 = responses['course2']
    course3 = responses['course3']
    pds = '1-9' if responses['period'] == 'option1' else '2-10'
    room1 = responses['room1']
    room2 = responses['room2']
    room3 = responses['room3']
    lunch1 = responses['pd1']
    lunch2 = responses['pd2']
    lunch3 = responses['pd3']
    years = responses['years']

    query = 'INSERT INTO responses VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (iden, course1, course2, course3, pds, room1, room2, room3, lunch1, lunch2, lunch3, years)
    c.execute(query)
    db.commit()

def addTeachers():
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    query = 'DROP TABLE IF EXISTS teachers'
    c.execute(query)

    query = 'CREATE TABLE teachers (email TEXT, first TEXT, last TEXT);'
    c.execute(query)

    f = open('data/teachers.csv')
    reader = csv.DictReader(f)
    for row in reader:
        email = row['Email address']
        first = row['First name'].capitalize()
        last = row['Last name'].capitalize()
        query = 'INSERT INTO teachers VALUES("%s", "%s", "%s");' % (email, first, last)
        c.execute(query)
    db.commit()
    f.close()

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
    
def addCourses():
    db = sqlite3.connect('data/data.db')
    c = db.cursor()

    query = 'DROP TABLE IF EXISTS courses'
    c.execute(query)

    query = 'CREATE TABLE courses (code TEXT, title TEXT);'
    c.execute(query)

    f = open('data/courses.csv')
    reader = csv.reader(f)
    for row in reader:
        course = row['Course']
        coursename = row['Course Title'].uppercase()
        query = 'INSERT INTO courses VALUES("%s", "%s");' % (course, coursename)
        c.execute(query)
    db.commit()
    f.close()

addTeachers()
addAdmins()
addCourses()

def getCourses(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT course1,course2,course3 FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    courses = c.fetchall()[0]
    
    return courses

def getPds(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT pds FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    pds = c.fetchall()[0][0]
    
    return pds

def getRooms(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT room1,room2,room3 FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    rooms = c.fetchall()[0]
    
    return rooms

def getLunch(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT lunch1,lunch2,lunch3 FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    lunches = c.fetchall()[0]
    
    return lunches
    
def getYears(email):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT years FROM responses WHERE email = '%s';" %(email)
    c.execute(q)
    years = c.fetchall()[0][0]
    
    return years

def getEmail( fname, lname ):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT email FROM teachers WHERE first = '%s' AND last = '%s';" %(fname.capitalize(), lname.capitalize())
    c.execute(q)
    email = c.fetchall()[0][0]
    
    return email

def getName( email ):
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    
    q = "SELECT first,last FROM teachers WHERE email = '%s';" %(email)
    c.execute(q)
    name = c.fetchall()[0]
    name = name[0] + " " + name[1]
    
    return name

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

print whoChoseWhat( 'lunch', 1, 4 )
print whoChoseWhat( 'pds', '', '1-9' )
