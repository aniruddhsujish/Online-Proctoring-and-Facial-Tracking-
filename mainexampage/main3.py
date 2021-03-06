
from flask import Flask, render_template,redirect, request, Response, make_response
from camera import VideoCamera
import os
from gevent.pywsgi import WSGIServer
import mysql.connector
import sys
from datetime import datetime



#import pyrebase
app = Flask(__name__)
#app.secret_key=os.urandom(24)
conn=mysql.connector.connect(host="remotemysql.com",user="B2cfkZqKMi",password="NoM3V5RW8q",database="B2cfkZqKMi")
#enter valid credentials from onlinemysql
cursor=conn.cursor()

@app.route('/faculty')
def homez():
    return render_template('sss.html')

@app.route('/home')
def home():
    return render_template('index1.html')

@app.route('/features')
def features():
    return render_template('Features.html')

@app.route('/contact',methods=['GET', 'POST'])
#@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/teacher')
def teacher():
    return render_template('teacherlogin.html')

@app.route('/exam')
def exam():
    return render_template('exam.html')

@app.route('/proctoring', methods= ['GET'])
def proctoring():
	cur = conn.cursor()
	cur.execute("SELECT * FROM alerts")
	data = cur.fetchall()
	return render_template('proctoring.html', data=data)

@app.route('/marks',methods=['POST','GET'])
def marks():
    marks=request.form.get('marks')
    email=request.form.get('email')

    cursor.execute("""INSERT INTO `faculty` (`email`,'marks') VALUES 
    ('{}','{}')""".format(email,marks))
    conn.commit()
    return "Marks registered successfully"

@app.route('/login_validation',methods=['POST','GET'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `login` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password)) 
    login=cursor.fetchall()
    
    if len(login)>0:
        resp = make_response(render_template('newindex.html'))
        resp.set_cookie("email",email)
        return resp
    else:
        return render_template('login.html', error_msg="Incorrect username or password. Try again.")

@app.route('/teacher_login_validation',methods=['POST','GET'])
def teacher_login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `teacher_login` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password)) 
    login=cursor.fetchall()
    
    if len(login)>0:
        resp = make_response(render_template('newindexteacher.html'))
        resp.set_cookie("email",email)
        return resp
        #return render_template('newindexteacher.html')
    else:
        return render_template('teacherlogin.html', error_msg="Incorrect username or password. Try again.")


def gen(camera,email):
    while True:
        
        if not alert == "": 
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("""INSERT INTO `alerts` (`email`,`alert`,`time`) VALUES ('{}','{}','{}')""".format(email,alert,dt_string))
            conn.commit()      
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed/<email>')
def video_feed(email):

    return Response(gen(VideoCamera(),email),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
    #app.run(host='0.0.0.0', port=8000, debug=True)
