import uuid
from flask import session

from common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.email = email,
        self.password = password

    @classmethod
    def get_by_email(cls,email):
        data = Database.find_one(collection='users', query={'email':email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, id):
        data = Database.find_one(collection='users', query={'_id':id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        else:
            return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            return True
        else:
            return False

    @staticmethod
    def login(email):
        session['email'] = email

    @staticmethod
    def logput():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def save_to_mongo(self):
        Database.insert(collection='users', data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'email':self.email,
            'password':self.password
        }
