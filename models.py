from serve import db

class User(db.Document):
    email = db.StringField(required=True)
    password = db.StringField(max_length=50, required=True)
    name = db.StringField(max_length=50)
class App(db.Document):
	userId = db.StringField(required=True)
	name = db.StringField(max_length=50, required=True)
	numberFunc = db.IntField(required=True)
	language = db.StringField(required=True,max_length=50)
class Function(db.Document):
	userId = db.StringField(required=True)
	AppId = db.StringField(required=True)
	dockerContID = db.StringField(required=True)
	#code = db.StringField(required=True)
	dependancies =  db.ListField(db.StringField(max_length=30)) #has a list of other function IDs
