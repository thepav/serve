from flask import Flask
from flask import render_template, url_for, redirect, abort, request
import os
import subprocess
from flask.ext.mongoengine import MongoEngine
from models import *
from pprint import pprint

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
	apps = []
	for app in App.objects(userId=pk):
		appDict = {}
		appDict['name'] = app.name
		appDict['numberFunc'] = app.numberFunc
		appDict['language'] = app.language
		appDict['id'] = app.id
		apps.append(appDict)

	return render_template('gallery.html', apps=apps,userid=pk)

@serve.route('/new_app/', methods=['POST'])
def newApp():
	if request.method == 'POST':
		userId = request.form['userid']
		name = request.form['name']
		numberFunc = 1
		language = 'Python'
		daApp = App(userId=userId, name=name, numberFunc=numberFunc,language=language)
		daApp.save()
		function = Function(AppId=str(daApp.id), userId=userId, name="HelloWorld.py", code="print(\"hello world\")")
		function.save()
		return redirect(url_for('gallery', pk = userId))
	else:
		return str(404)

@serve.route('/newfunc/',methods=['POST'])
def newFunc():
	if request.method == 'POST':
		userId = request.form['userid']
		AppId = request.form['appid']
		code = request.form['code'].strip()
		name = request.form['name']
		appdoe = App.objects(id=AppId)[0]
		appdoe.numberFunc += 1
		appdoe.save()
		function = Function(AppId=AppId, userId=userId, name=name, code=code) # STILL NEED TO WORK OUT DEPENDENCIES!
		function.save()

		return redirect(url_for('gallery', pk = userId))

@serve.route('/dash/<appid>/')
def dashboard(appid):
	if request.method == 'GET':
		theapp = None
		for app in App.objects:
			if str(app.id) == appid:
				theapp = app
	return render_template("dashboard.html", app=theapp, functions=Function.objects(AppId=str(theapp.id)))


@serve.route('/updateApp/', methods=['POST'])
def updateApp():
	if request.method == 'POST':
		appid = request.form['appid']
		newName = request.form['name']
		theapp = None #hacky way to deal with stringification
		for app in App.objects:
			if str(app.id) == appid:
				theapp = app
		theapp.name = newName
		theapp.save()
		return redirect(url_for("dashboard", appid=theapp.id))

@serve.route('/updateCode/', methods=['POST'])
def updateCode():
	if request.method == 'POST':
		fid = request.form['fid']
		newName = request.form['name']
		code = request.form['text']
		func = None #hacky way to deal with stringification
		for funky in Function.objects:
			if str(funky.id) == str(fid):
				func = funky
		func.code = code
		func.name = newName
		func.save()
		return True

@serve.route('/run/<functionid>/')
def run(functionid): #need userid,appid,functionid
	print 'something fucking happened' 	
	print 'got here too'
	#functionid = request.form['functionid']
	print 'but probably not here'
	function = Function.objects(id=str(functionid))
	print '\n\n'+function+'\n\n'
	code = function.code
	params = parseCode(code)

	print '\n\nparamsdoe '+params+'\n\n'
	values = {}
	for param in params:
		values[param] = request.form[param]

	sansfirstline = '\n'.join(code.split('\n')[1:-1]) # and last row
	sansfirstline = textwrap.dedent(sansfirstline)
	lastline = code.split('\n')[-1]
	lastline = lastline.replace('return', 'print')

	firstline = ''
	for param in params:
		firstline += param +'='+values[param] + '\n'
	code = firstline + sansfirstline +lastline
	print '\n\n'+code+'\n\n'
	
	os.popen('rm code.py');
	f = open('code.py','w')
	f.write(code)
	f.close()
	print '\n\n code.py created. \n\n'

	os.popen('rm Dockerfile');
	f = open('Dockerfile','w')
	f.write('FROM python \n ADD ./code.py /usr/src/python/code.py')
	f.close()
	os.popen('sudo docker build -t imagedoe . & sudo docker run imagedoe code.py > out.txt')
	
	print ('\n\n Docker shit doneski. \n\n')

	f = open('out.txt','r')
	result = f.read().strip()
		
	print '\n\n'+result+'\n\n'
	return result

def parseCode(code):
	import StringIO
	buf = StringIO.StringIO(code)
	definition = buf.readline().strip()
	left  = definition.index('(')
	right = definition.index(')')
	params = definition[left+1:right]
	params = params.replace(' ','')
	params = params.split(',')

	return params


if __name__ == "__main__":
    serve.debug = True
    serve.run()
