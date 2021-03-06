from flask import Flask
from flask import render_template, url_for, redirect, abort, request
import os
import subprocess
from flask.ext.mongoengine import MongoEngine
from models import *
import config
import requests
import sendgrid
db = MongoEngine()
sg = sendgrid.SendGridClient(config.sendgrid_user, config.sendgrid_pw)

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
		password = request.form['password']
		name = request.form['name']
		user = User(email=email, password=password,name=name,paid=1)

		user.save()
		message = sendgrid.Mail()
		message.add_to(email)
		message.set_subject("Welcome to Serve!")
		message.set_html(render_template("welcomemail.html", name=name))
		message.set_from("Serve Team (team@serveapp.cloudapp.com)")
		a, b = sg.send(message)
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
	user = None
	for us in  User.objects(id=pk):
		if str(us.id) == str(pk):
			user = us

	return render_template('gallery.html', apps=apps,userid=pk, user=user,numActApps = len(apps), numAppAvail=(int(user.paid) * 5))

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
		types = []
		appdoe = App.objects(id=AppId)[0]
		appdoe.numberFunc += 1
		appdoe.save()
		function = Function(AppId=AppId, userId=userId, name=name, code=code, types=types) # STILL NEED TO WORK OUT DEPENDENCIES!
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
		print 'update1'
		fid = request.form['fid']
		print 'update2'
		newName = request.form['name']
		print 'update3'
		code = request.form['text']
		print 'update4'
		types = request.form['types']
		print types
		types = types.strip().split(',')
		print 'update6'	
		func = None #hacky way to deal with stringification
		for funky in Function.objects:
			if str(funky.id) == str(fid):
				func = funky
		print 'update7'
		func.types = types
		print func.types
		func.code = code
		print 'update9'
		func.name = newName
		print 'update10'
		func.save()
		print 'update11'
		return 200
	else:
		return 404

@serve.route('/options/<userId>', methods=["GET"])
def options(userId):
	return render_template("buy.html", userId = userId)

@serve.route('/pay/<userId>')
def payment(userId):
	return redirect("https://api.venmo.com/v1/oauth/authorize?client_id="+config.uid+"&scope=make_payments%20access_profile&response_type=token&uri_redirect=%s".format("http://serveapp.cloudapp.net/venmo/%s".format(userId)));

@serve.route('/venmo/<userId>')
def venmo():
	q = {"access_token": request.url.split("=")[1], "phone":config.phone, "note":"Serve payment", "amount": "2", "audience":"private"}
	r = requests.post("https://api.venmo.com/v1/payments", data=q)
	user = None
	for us in User.objects:
		if str(us.id) ==userId:
			user = us

	message = sendgrid.Mail()
	message.add_to(user.email)
	message.set_subject("We're Serving you even better!")
	message.set_html(render_template("purchasemail.html", name=user.name))
	message.set_from("Serve Team (team@serveapp.cloudapp.com)")
	a, b = sg.send(message)
	return redirect(url_for('gallery', pk=5)) 

@serve.route('/run/<functionid>/', methods=['GET'])
def run(functionid): #need userid,appid,functionid
	print 'something fucking happened' 	
	print 'got here too'
	#functionid = request.form['functionid']
	print 'but probably not here'
	print functionid
	funct = None
	for fun in Function.objects:
		print fun.id
		if str(fun.id) == str(functionid):
			funct = fun
	#print '\n\n'+function+'\n\n'
	code = funct.code
	types = funct.types
	params = parseCode(code)

	print '\n\nparamsdoe '+str(params)+'\n\n'
	values = {}
	for param in params:
		values[param] = request.args.get(param)
	
	import textwrap

	sansfirstline = '\n'.join(code.split('\n')[1:-1]) # and last row
	sansfirstline = textwrap.dedent(sansfirstline)
	lastline = code.split('\n')[-1]
	lastline = lastline.replace('return', 'print')
	lastline = textwrap.dedent(lastline)
	print 'last:'+lastline
	if sansfirstline.strip() == '':
		sansfirstline = ''

	firstline = ''
	count = 0

	for param in params:
		firstline += param +"="+types[count]+"('"+values[param] + "')\n"
		count+=1
		
	code = firstline + sansfirstline +lastline
	print '\ncode:\n'+code+'\n\n'

	f = open('codey.py','w')
	f.write(code)
	f.close()

	f = open('codey.py','r')
	print 'file: \n'+f.read();
	print '\n\n codey.py created. \n\n'
	
	subprocess.call('pwd')	

	subprocess.call('sudo docker run -v /home/azureuser/serve/codey.py:/usr/src/python/codey.py python:2.7.7 python /usr/src/python/codey.py > out.txt 2>&1', shell=True)
	
	print ('\n\n Docker shit doneski. \n\n')

	f = open('out.txt','r')
	result = f.read().strip()
	f.close()
	
		
	print '\n\n'+result+'\n\n'
	return str(result)

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
