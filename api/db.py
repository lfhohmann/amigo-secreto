import os

from mongoengine import DictField, Document, connect

connect(host=os.getenv("dbhost"))


class Data(Document):
    data = DictField()
