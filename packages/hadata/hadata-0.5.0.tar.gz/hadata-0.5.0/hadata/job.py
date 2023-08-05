from mongoengine import Document, StringField, ObjectIdField, DateTimeField, IntField, FloatField, BooleanField


class Job(Document):
    name = StringField(required=True)
    organization_id = StringField(required=False)
    filename = StringField(required=True)
    file_hash = StringField(required=True)
    status = StringField(required=True)
    transcript = StringField(required=False)
    topic = StringField(required=False)
    user_id = ObjectIdField(required=False)
    creation_date_time = DateTimeField(required=False)

    def set_status(self, status):
        self.status = status
        job_history = JobHistory()
        job_history.job_id = self.file_hash
        job_history.job_status = status
        now = datetime.now()  # current date and time
        job_history.status_date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        job_history.save()


class JobHistory(Document):
    job_id = StringField(required=True)
    job_status = StringField(required=True)
    status_date_time = StringField(required=True)
