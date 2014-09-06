from serve import db

class User(db.Document):
    email = db.StringField(required=True)
    password = db.StringField(max_length=50, required=True)
    name = db.StringField(max_length=50)
