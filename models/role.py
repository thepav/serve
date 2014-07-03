from mongoengine import *
from flask.ext.security import RoleMixin

class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)
