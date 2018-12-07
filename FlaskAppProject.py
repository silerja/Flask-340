__author__ = 'Tony Teate'

__author__ = 'Edits by. Joe Siler and Alex Martin'

#imports
import sqlite3
from flask import Flask, render_template
from flask import request, redirect, url_for

#instantiate
app = Flask(__name__)
# route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('celebrities.db')
        c = conn.cursor()
        find_user = ("SELECT * FROM members where username = ? AND password = ?")
        c.execute(find_user, [(username), (password)])
        results = c.fetchall()
        if results:
            for i in results:
                return redirect(url_for('info'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.htm', error=error)

@app.route('/info', methods=['GET', 'POST'])
def info():
    memberID = None
    firstname = ''
    lastname = ''
    age = None
    email = ''
    bio = ''
    success = False

    if request.method == 'GET':
        conn = sqlite3.connect('celebrities.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM members''')
        row = c.fetchone()

        if row:
            memberID = row[0]
            firstname = row[1]
            lastname = row[2]
            age = row[3]
            email = row[4]
            bio = row[5]

        conn.close()

    if request.method == 'POST':
        #get the data from the forms and store it in variables
        #this uses the request method to get the data from named elements on the form
        memberID=request.form['memberID']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        email = request.form['email']
        bio = request.form['bio']
        success = True
        # now store the data from the form into the database
        conn = sqlite3.connect('celebrities.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM members''')
        row = c.fetchone()
        if row: #if the row exist, update the data in the db
            c.execute('''UPDATE members SET firstname = ?, lastname = ?, age = ?, email = ?, bio = ? WHERE memberID=?''',
                      (firstname, lastname, age, email, bio, memberID))
        else: #if the row does not exist, insert data into row
            c.execute('''INSERT INTO members VALUES (?, ?, ?, ?, ?, ?)''',
                      (memberID, firstname, lastname, age, email, bio))
        conn.commit()
        conn.close()
    return  render_template('profile.htm', memberID=memberID, firstname=firstname, lastname=lastname, age=age, email=email, bio=bio, success=success)

@app.route('/view_all_celebs')
def view_all():
    celebID=None
    firstname = ''
    lastname = ''
    age = ''
    email = ''
    photo = ''
    bio = ''

    conn = sqlite3.connect('celebrities.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM celebs ORDER BY celebID''')
    rows = c.fetchall()
    conn.close()
    #return
    return render_template('view_all_celebs.htm',
rows=rows)

@app.route('/view_one_celeb')
def viewone():
    celebID = ''
    firstname = ''
    lastname = ''
    age = ''
    email = ''
    photo = ''
    bio = ''

    conn = sqlite3.connect('celebrities.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Celebs where celebID = 3")
    rows = c.fetchone()
    celebID = rows[0]
    firstname = rows[1]
    lastname = rows[2]
    age = rows[3]
    email = rows[4]
    photo = rows[5]
    bio = rows[6]

    conn.close()

    return render_template("view_one_celeb.html", celebID = celebID, firstname = firstname,
                           lastname = lastname, age = age, email = email, photo = photo, bio = bio)

def get(request):
    pass

def post(request):
    pass

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":
    app.run(debug=False)
