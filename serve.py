from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.route("/")
def hello():
	#convert hash to username
	# username = getUsername(userHash)
 #    return render_template('process.html', username=username)
 	stuff = os.popen("ls -l").read()
 	print '\n' in stuff
	return stuff

def getUsername(userHash):
	return 'Pav'

if __name__ == "__main__":
    app.debug = True
    app.run()
