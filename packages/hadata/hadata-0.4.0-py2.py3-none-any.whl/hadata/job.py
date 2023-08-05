from mongoengine import Document, StringField, ObjectIdField, DateTimeField, IntField, FloatField, BooleanField


class JobHistory(Document):
    job_id = StringField(required=True)
    job_status = StringField(required=True)
    status_date_time = StringField(required=True)
