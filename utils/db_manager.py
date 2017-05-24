import sqlite3, hashlib, random

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

    if (len(info) > 0):
        return True #teacher already exists in database
    else:
        return False #if false it should ask a teacher for their name + department, then add them to the db

#DONT REALLY NEED
#we have a CSV with all the teachers (AP included)
def addTeach( fname, lname, dept, email ):
    db = sqlite3.connect("data/data.db")
    users = db.cursor()

    q = '''INSERT INTO teachers( fname, lname, dept, email ) VALUES("%s", "%s", "%s", "%s");''' % ( fname, lname, dept, email )
    users.execute(q)

    q = "SELECT id FROM teachers WHERE email = \"%s\";" % ( email ) #get the id
    users.execute(q)
    iden = users.fetchall()[0][0]
    
    q = "INSERT INTO response( id ) VALUES(%s);" % ( iden ) #create an empty response entry for them
    users.execute(q)
    db.commit()
    return True #success

def getID( email ):
    pass #keep email in the session?

def editResponse( iden, c1, c2, c3, wp, r1, r2, r3, l1, l2, l3, yrs ):
    pass #find matching id and insert values
