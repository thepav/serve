from flask import Flask
from flask import render_template, url_for, redirect, abort, request
import os
import subprocess
from flask.ext.mongoengine import MongoEngine
from models import *

db = MongoEngine()

serve = Flask(__name__)
#serve.config.from_pyfile('the-config.cfg')
serve.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': 'localhost',
    'port': 27017
}

db.init_app(serve)


@serve.route("/")
def hello():
	#convert hash to username
	# username = getUsername(userHash)
	# subprocess.call(['python server.py &'], shell=True)
 # 	print os.popen("jobs -l").read()
	stuff2 = os.popen("ps -fA | grep python").read().replace('\n','<br>')
 	stuff2 = stuff2 + str('<br><br><br>') + os.popen('ls').read()
	return render_template('index.html', stuff=stuff2)

@serve.route("/auth/", methods='POST')
def auth():
	if request.method == 'POST':
			email = request.form['email']
			password = request.form['password']

			user = User.objects(email=email, password=password)

			return redirect(url_for('gallery'),pk=user._id);
    	else:
			return render_template('login_failed.html');
@serve.route('/login/')
def login():
	return render_template('login.html')

@serve.route('/signup/')
def signup():
        return render_template('signup.html')

@serve.route('/new_signup/', methods='POST')
def newSignup():
	email = request.form['email']
	password = request.form['password']
	name = request.form['name']
	user = User(email=email, password=password,name=name)
	user.save()

	return redirect(url_for('gallery'),pk=user._id);

@serve.route('/gallery/<pk>')
def dashboard(pk):
	return pk;








if __name__ == "__main__":
    serve.debug = True
    serve.run()
