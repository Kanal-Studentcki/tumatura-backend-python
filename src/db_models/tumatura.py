from datetime import datetime, timedelta

from mongoengine import Document, EmailField, StringField, IntField, ListField, EmbeddedDocumentField, EmbeddedDocument, \
    DateTimeField


### Collection: users
class UserRole(EmbeddedDocument):
    role_id = IntField(required=True)
    exp_date = DateTimeField(default=(datetime.now() + timedelta(weeks=1)))


class Users(Document):
    customer_id = IntField()
    email = EmailField()
    discord = StringField()
    roles = ListField(EmbeddedDocumentField(UserRole), default=[])

    def __getitem__(self, index):
        return self.discord


### Collection: roles
class Roles(Document):
    role_id = IntField(required=True)
    role_name = StringField()
