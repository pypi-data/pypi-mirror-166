from mongoengine import Document, EmailField, StringField, ObjectIdField, DateTimeField, IntField, FloatField, BooleanField


class MongoUser(Document):
    meta = {'collection': 'user'}
    _id = ObjectIdField
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    organization_id = StringField(required=True)
    profile_type = IntField(required=True)
    is_verified = BooleanField(required=True, default=False)


class MongoUserAssessment(Document):
    meta = {'collection': 'user_assessment'}
    enabled = BooleanField(required=True, default=True)
    score = IntField(required=True, default=0)
    status = StringField(required=True)
    user_id = ObjectIdField(required=True)
    assessment_id = ObjectIdField(required=True)
    start_time = DateTimeField(required=False)
    end_time = DateTimeField(required=False)
    marked = BooleanField(required=True, default=False)
