from mongoengine import Document, StringField


class Account(Document):
    user = StringField()
    find_phone_status = StringField()
    alarm_status = StringField()
    register_time = StringField()


class History(Document):
    user = StringField()
    action = StringField()
    time = StringField()
