from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.route("/")
def hello():
	#convert hash to username
	# username = getUsername(userHash)
    #    return render_template('process.html', username=username)
 	stuff = os.popen("python -m simplehttpserver_test/server.py 7000").read()
 	stuff2 = os.popen("ps").read()
 	
 	# python -m simplehttpserver_test/server.py 80
	return stuff2

def getUsername(userHash):
	return 'Pav'

if __name__ == "__main__":
    app.debug = True
    app.run()
