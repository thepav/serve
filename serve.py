from flask import Flask
from flask import render_template
 	from subprocess import call

app = Flask(__name__)

@app.route("/<userHash>")
def hello(userHash=None):
	#convert hash to username
	# username = getUsername(userHash)
 #    return render_template('process.html', username=username)
	return call(["ls", "-l"])

def getUsername(userHash):
	return 'Pav'

if __name__ == "__main__":
    app.debug = True
    app.run()
