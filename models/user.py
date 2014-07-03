from mongoengine import *
from flask.ext.security import UserMixin
from role import Role
from script import Script

class User(Document, UserMixin):
    email = EmailField(max_length=255)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
