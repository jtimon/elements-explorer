# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from mintools import ormin

# TODO move SECRET_KEY away
SECRET_KEY = 'SECRET_KEY'

class User(ormin.Model):
    username = ormin.StringField(unique=True)
    email = ormin.StringField(unique=True)
    password_hash = ormin.StringField(required=False)

    def new_id(self):
        self.id = self.username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self):
        s = Serializer(SECRET_KEY, expires_in = 600)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        return User.get(data['id'])

    def json(self, full=False):
        json = super(User, self).json(full)
        if full:
            json['token'] = self.generate_token()
            del json['password_hash']
            del json['email']
        return json

class Register(User):
    password = ormin.StringField()
    password2 = ormin.StringField()

    @staticmethod
    def get_name():
        return 'user'

    def validate(self):
        if super(Register, self).validate():
            return self.errors

        if self.password != self.password2:
            self.errors['password'] = "The passwords don't match."

        return self.errors

    def insert(self):
        user = User(self.json(False))
        user.hash_password(self.password)
        return user.insert()

class UpdateUser(User):
    password = ormin.StringField()
    new_password = ormin.StringField(required=False)

    def validate(self):

        user = User.search({'username': self.username})
        if not user.verify_password(self.password):
            self.errors['password'] = 'Incorrect password.'
            return self.errors

        # Prevent unique validations from raising
        self.username = '_dummy'
        if user.email == self.email:
            self.email = '_dummy'

        super(UpdateUser, self).validate()
        return self.errors

    def update(self):
        user = User(self.json())
        if self.new_password:
            user.hash_password(self.new_password)
        return user.update()
