from common.database import Database
import uuid
import datetime

class Post(object):

    def __init__(self, blog_id, title, content, author_name, created_date = datetime.datetime.utcnow(),_id=None):
        self._id = uuid.uuid4().hex if _id is None else _id,
        self.blog_id = blog_id,
        self.title = title,
        self.content = content
        self.author_name = author_name,
        self.created_date = created_date

    def save_to_mongo(self):
        Database.insert(collection = 'posts', data= self.json())

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts',query={'_id':id})
        return cls(**post_data)

    @staticmethod
    def from_blog(blog_id):
        return [post for post in Database.find(collection='posts', query={'blog_id':blog_id})]
    def json(self):
        return {
            'id': self._id,
            'blog_id': self.blog_id,
            'title': self.title,
            'content':self.content,
            'author_name': self.author_name,
            'created_date': self.created_date
        }
