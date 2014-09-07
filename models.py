from serve import db

class User(db.Document):
    email = db.StringField(required=True)
    password = db.StringField(max_length=50, required=True)
    name = db.StringField(max_length=50)
    paid = db.BooleanField()
class App(db.Document):
	userId = db.StringField(required=True)
	name = db.StringField(max_length=50, required=True)
	numberFunc = db.IntField(required=True)
	language = db.StringField(required=True,max_length=50)
class Function(db.Document):
	userId = db.StringField(required=True)
	AppId = db.StringField(required=True)
	name = db.StringField(max_length=30)
	code = db.StringField(required=True)
<<<<<<< HEAD
	types = db.ListField(db.StringField(max_length=20, required=True))
=======
	types = db.ListField(db.StringField(max_length=30))
>>>>>>> 92dcddb758bc86e48cb08e20bc8f3faa2d0c2741
	dependancies =  db.ListField(db.StringField(max_length=30)) #has a list of other function IDs
