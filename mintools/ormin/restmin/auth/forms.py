
from mintools import ormin

class LoginForm(ormin.Form):
    username = ormin.StringField()
    password = ormin.StringField()
