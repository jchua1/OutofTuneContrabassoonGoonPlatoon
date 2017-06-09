# Stuyvesant Staff Faculty Scheduling App

#### Team  Out of Tune Contrabassoon Goon Platoon
- Jason Chua (Project Manager)
- Jordan Chan
- Lawrence Liu
- Fortune Soleil

A Flask driven app that will allow faculty to submit their scheduling preferences online. Administrators will have access to the accumulated responses and will be able to view them in various ways, allowing easier scheduling and having all teacher preferences readily available in one place. We would also like to make graphs that allows administrators to see at a glance what periods or classes are most requested.

## Running the Faculty Scheduling App:
1) Install module for oauth: `$ pip install oauth2client`

2) Add teachers.csv, admins.csv, and courses.csv to data directory.

- Format of teachers.csv:  
  Header: 'Email address','First name','Last name'  
  <STUY.EDU EMAIL>,<FIRST NAME>,<LAST NAME>
- Format of admins.csv:
  No Header  
  <STUY.EDU EMAIL>  
- Format of courses.csv:  
  Header: 'Course', 'Course Title'  
  <COURSE CODE>, <COURSE NAME>  
- Make sure the format and names of each file are correct or else the information will not be added to the database. This should be only  done when the FINAL VERSION of each csv file is in the data directory.

3) Populate the database. This should only be done when the FINAL VERSION of each CSV file for the upcoming semester is in the data directory.

- Adding teachers: `$ scheduling/utils/db_manager.py teachers`

- Adding admins: `$ scheduling/utils/db_manager.py admins`

- Adding courses: `$ scheduling/utils/db_manager.py courses`

4) That's it! Run the application using: `$ scheduling/__init__.py`
