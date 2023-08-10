from django.db import models
from mongoengine import Document, StringField, FloatField, BooleanField, ListField

class MenuItem(Document):
    dish_name = StringField(required=True)
    price = FloatField(required=True)
    availability = BooleanField(required=True)

class Order(Document):
    customer_name = StringField(required=True)
    dish_ids = ListField(StringField())  # List of dish IDs
    status = StringField()

