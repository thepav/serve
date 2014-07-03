from mongoengine import *

default_script = 'print \'Hello, world!\''
status_choices = ('OK', 'Warning', 'Error')
language_choices = ('Python')

class Script(Document, RoleMixin):
    name = StringField(max_length=255)
    description = StringField(max_length=1000)
    url = StringField()
    script = StringField(required=True, default=default_script)
    language = StringField(required=True, default='Python', choices=langauge_choices)
    log = StringField()
    started = BooleanField(required=True, default=False)
    status = StringField(required=True, default='OK', choices=status_choices)
