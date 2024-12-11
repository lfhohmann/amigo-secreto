import os

from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    Document,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
    connect,
)

connect(host=os.getenv("dbhost"))


class Amigo(Document):
    name = StringField(required=True)
    id_ = StringField(required=True)
    people = ListField(StringField())
    chosen = StringField(required=True)
