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

@serve.route("/auth/", methods=['POST'])
def auth():
	if request.method == 'POST':
			email = request.form['email']
			password = request.form['password']

			dauser = None
			for user in User.objects:
   				print user.name + ',' + user.email + ',' + user.password
   				if user.email == email and user.password == password:
   					dauser = user
   			if dauser == None:
   				return render_template('login_failed.html');
   			else:
#			return str(dauser) +'<br>'+ email+'<br>'+password + '<br>' + str(User.objects())
				return redirect(url_for('gallery',pk=dauser.id));
    	else:
			return render_template('login_failed.html');
@serve.route('/login/')
def login():
	return render_template('login.html')

@serve.route('/signup/')
def signup():
        return render_template('signup.html')

@serve.route('/new_signup/', methods=['POST'])
def newSignup():
	if request.method == 'POST':
		email = request.form['email']
		print '1'
		password = request.form['password']
		print '2'
		name = request.form['name']
		print '3'
		user = User(email=email, password=password,name=name)
		print '4'
		user.save()
		print 'done signup'
		return redirect(url_for('gallery',pk=user.id));
	else:
		redirect(url_for('signup'))
		
@serve.route('/gallery/<pk>',)
def gallery(pk):
	# give me something like this, where apps are all of the user's active apps
	apps = [{"name":"test", "url": "/"+str(pk)+"/test", "dash":"/dash/"+str(pk)+"/test"}, {"name":"test", "url": "/"+str(pk)+"/test", "dash":"/dash/"+str(pk)+"/test"}, {"name":"test", "url": "/"+str(pk)+"/test", "dash":"/dash/"+str(pk)+"/test"}, {"name":"test", "url": "/"+str(pk)+"/test", "dash":"/dash/"+str(pk)+"/test"}]
	return render_template('gallery.html', apps=apps,userid=pk)

@serve.route('/new_app/', methods=['POST'])
def newApp():
	if request.method == 'POST':
		userId = request.form['userid']
		name = request.form['name']
		numberFunc = 0
		language = 'Python'
		daApp = App(userId=userId, name=name, numberFunc=numberFunc,language=language)
		daApp.save()
		return redirect(url_for('gallery', pk = userId))
	else:
		return str(404)

@serve.route('/newfunc/<userid>/<appid>/<functionid>/',methods=['POST'])
def newFunc(userid,appid,functionid):
	if request.method == 'POST':
		AppId = request.form['appid']
		code = request.form['code']
		daApp = App(userId=userId, name=name, numberFunc=numberFunc,language=language)
		daApp.save()
		return redirect(url_for('gallery', pk = userId))
	os.popen('')


@serve.route('/run/<userid>/<appid>/<functionid>/', methods=['GET'])
def run(userid,appid,functionid):
	return str(404)


if __name__ == "__main__":
    serve.debug = True
    serve.run()
