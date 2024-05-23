
from flask import Flask, render_template, request, session, redirect, flash
import mysql.connector
import os
import re
from chatbot import chatbot_response


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.static_folder = 'static'

@app.route('/index')
def home():
    if 'id' in session:
        return render_template("index.html")
    else:
        return redirect('/')

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template("register.html")

@app.route('/aboutus')
def aboutus():
    return render_template("Aboutus.html")

@app.route('/suggestion')
def suggestion():
    return render_template("suggestion.html")



#database connectivity
conn=mysql.connector.connect(host='localhost',user='root',password='',database='techno')
cur=conn.cursor()

@app.route('/add_user',methods=['POST','GET'])
def register():
    mesage = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'address' in request.form and 'phone'in request.form and 'email'in request.form and 'password' in request.form :
      firstname=request.form['firstname']
      lastname = request.form['lastname']
      address = request.form['address']
      phone = request.form['phone']
      email=request.form['email']
      password=request.form['password']
      
      cur.execute("""SELECT * FROM `register` WHERE `email` LIKE '{}' """.format(email))
      account = cur.fetchone()
      if account:
            mesage = 'Email Account already exists !'
      
      

      elif firstname.isdigit() or lastname.isdigit():
          mesage= 'Invalid Entry for FirstName  or LastName!' 
       
    
      elif not firstname or not lastname or not address or not phone or not email or not password :
            mesage = 'Please fill out the form !'

      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
           
      else:
          cur.execute("""INSERT INTO  register(firstname,lastname,address,phone,email,password) VALUES('{}','{}','{}','{}','{}','{}')""".format(firstname,lastname,address,phone,email,password))
          conn.commit()
          mesage = 'You have successfully registered !'
          return render_template('login.html',mesage=mesage)
    elif request.method == 'POST':
       mesage = 'Please fill out the form !'

    return render_template('register.html', mesage = mesage)




@app.route('/login_validation',methods=['POST','GET'])
def login_validation():
     mesage = ''
     if request.method == 'POST' and 'email'in request.form and 'password' in request.form :
       email=request.form['email']
       password=request.form['password']

       cur.execute("""SELECT * FROM `register` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
       users = cur.fetchall()
       if len(users)>0:
        session['id']= users[0][0]
        mesage='You were successfully logged in!'
        return render_template('index.html',mesage= mesage)
       else:
         mesage='Invalid credentials !!!'
     return render_template('login.html',mesage= mesage)
    #return  render_template('/')

@app.route('/feedback', methods=['POST','GET'])
def feed():
     mesage = ''
     if request.method == 'POST' and 'email' in request.form and 'message' in request.form :
       email=request.form['email']
       message=request.form['message']
       if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
            return  render_template('suggestion.html', mesage= mesage)
       else:
          cur.execute("""INSERT INTO  suggestion(email,message) VALUES('{}','{}')""".format(email,message))
          conn.commit()
          mesage='You suggestion is succesfully sent!'
          return render_template('suggestion.html', mesage = mesage)
     elif request.method == 'POST':
       mesage='Please fill out the form !'
       return render_template('suggestion.html', mesage = mesage)




@app.route('/clear')
def clear():
      return redirect('/')

@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')




@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)
    
if __name__ == "__main__":
    app.debug = True
    app.run()