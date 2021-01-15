from mongoengine import (
    StringField,
    Document,
    DecimalField,
    DateTimeField,
    BooleanField,
    ReferenceField,
    ListField,
)
import datetime


class Asset(Document):
    type = StringField(required=True, max_length=20)
    symbol = StringField(required=True, max_length=10, unique_with="type")
    open = DecimalField()
    close = DecimalField()
    last = DecimalField()
    time = DateTimeField(default=datetime.datetime.now)


class User(Document):
    user_id = StringField(required=True, max_length=25)
    first_name = StringField(required=True, max_length=25)
    last_name = StringField(required=True, max_length=25)


class Order(Document):
    type = BooleanField(default=True)
    asset = ReferenceField(Asset)
    user = ReferenceField(User)
    price = DecimalField(precision=2)
    quantity = DecimalField()
    charges = DecimalField(precision=2)
    time = DateTimeField(default=datetime.datetime.now)


class Position(Document):
    orders = ListField(ReferenceField(Order))
    asset = ReferenceField(Asset)
