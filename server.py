from flask import Flask, redirect, render_template, flash,request
from mysqlconnection import MySQLConnector
app=Flask(__name__)
mysql=MySQLConnector(app,'friends')
app.secret_key="123"
@app.route('/')
def index():
    emails=mysql.query_db("SELECT * FROM emails")
    print emails
    return render_template('index.html')
@app.route('/create', methods=['POST'])
def create():
    print request.form['email']
    current_email=request.form['email']
    query="SELECT e.email FROM emails e Where email=:email"
    data={
        "email": current_email
    }
    email_query=mysql.query_db(query,data)
    if len(email_query) >1 :
        flash('Email is not valid','red')
    else:
        flash('The email address you entered "{}" is valid. Thank you!'.format(current_email) , 'green')
        query="INSERT INTO emails (email,created_at,updated_at) VALUES (:email,now(),now())"
        data={
            "email": current_email
        }
        mysql.query_db(query,data)
        return redirect('/success')
    return redirect('/')
@app.route('/success')
def show():
    emails=mysql.query_db("SELECT email, DATE_FORMAT(created_at,'%m %d %Y %h:%i %p') AS created_at FROM emails")
    return render_template('show.html',emails=emails)

app.run(debug=True)
