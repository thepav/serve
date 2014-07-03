from flask import Flask
from flask import render_template
import os
import server

app = Flask(__name__)

@app.route("/")
def hello():
	#convert hash to username
	# username = getUsername(userHash)
    #    return render_template('process.html', username=username)
 	#os.popen("python server.py &")
 	server.run(6000)
 	print os.popen("jobs -l").read()
	stuff2 = os.popen("jobs -l").read()
 	stuff2 = stuff2 + str('<br><br><br>') + os.popen('ls').read()
 	
	#print stuff2
 	# python -m simplehttpserver_test/server.py 80
	return stuff2

def getUsername(userHash):
	return 'Pav'

if __name__ == "__main__":
    app.debug = True
    app.run()
