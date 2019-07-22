import uuid

from src.models.post import Post
from common.database import Database
import datetime


class Blog(object):

    def __init__(self, title, description, author, _id=None):
        self.title =title,
        self.description = description,
        self.author = author,
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(
            blog_id=self._id,
            title=title,
            content=content,
            author_name=self.author,
            created_date = date
        )
        post.save_to_mongo()

    def get_post(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blog', data=self.jason())


    def jason(self):
        return {
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'id':self._id
        }

    @classmethod
    def from_mongo(cls,id):
        blog_data = Database.find_one(collection='blog', query={'_id':id})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blog', query={'author_id':author_id})
        return [cls(**blog)for blog in blogs]
