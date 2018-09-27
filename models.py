import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config

DATABASE = SqliteDatabase(config.DATABASE)
HASHER = PasswordHasher()


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()

        try:
            cls.select().where(
                (cls.email == email) | (cls.username ** username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = user.set_password(password)
            user.save()

            return user

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.password, password)

    def generate_auth_token(self, expiration=600):
        serializer = Serializer(config.SECRET_KEY, expires_in=expiration)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


class Todo(Model):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now())
    user = ForeignKeyField(User, related_name="user_set")

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
