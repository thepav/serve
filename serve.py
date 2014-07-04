from flask import Flask
from flask import render_template
import os
import subprocess

serve = Flask(__name__)

@serve.route("/")
def hello():
	#convert hash to username
	# username = getUsername(userHash)
	# subprocess.call(['python server.py &'], shell=True)
 # 	print os.popen("jobs -l").read()
	stuff2 = os.popen("ps -fA | grep python").read().replace('\n','<br>')
 	stuff2 = stuff2 + str('<br><br><br>') + os.popen('ls').read()
	return render_template('index.html', stuff=stuff2)

def getUsername(userHash):
	return 'Pav'

if __name__ == "__main__":
    serve.debug = True
    serve.run()
