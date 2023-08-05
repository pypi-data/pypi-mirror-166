from mongoengine import Document, StringField, ObjectIdField, DateTimeField, IntField, FloatField, BooleanField


class MongoUserAssessmentsQuestionAnswerStatusHistory(Document):
    meta = {'collection': 'user_assessment_question_answer_status_history'}
    user_assessment_question_answer_id = ObjectIdField(required=True)
    status = StringField(required=True)
    created_datetime = DateTimeField(required=True)


class MongoUserAssessmentsQuestionAnswer(Document):
    meta = {'collection': 'user_assessment_question_answer'}
    user_id = ObjectIdField(required=True)
    assessment_id = ObjectIdField(required=True)
    question_answer_id = ObjectIdField(required=True)
    user_assessment_id = ObjectIdField(required=False)
    score = IntField(required=False)
    time_taken = IntField(required=False)
    time_started = DateTimeField(required=False)
    time_completed = DateTimeField(required=False)
    time_ping = DateTimeField(required=False)
    user_answer = StringField(required=False)
    system_answer = StringField(required=False)
    status = StringField(required=False)
    sort_order = IntField(required=False)
    system_question = StringField(required=True)
    max_score = IntField(required=False)
    question_type = StringField(required=False)
    allowed_time = IntField(required=False)
    face_detected = FloatField(required=False)
    similarity_score = FloatField(required=False)
    is_correct = BooleanField(required=False)
    personal_notes = StringField(required=False)