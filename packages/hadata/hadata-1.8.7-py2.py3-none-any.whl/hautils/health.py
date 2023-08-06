import datetime
import json

from hadata.meta import MongoDiagnostics


def get_diagnostic_record(service):
    return MongoDiagnostics.objects(service=service).order_by('-timestamp').first()


def add_diagnostic_record(service, remark):
    diagnostic = MongoDiagnostics.objects(service=service).first()
    if diagnostic is not None:
        diagnostic.timestamp = datetime.datetime.now().timestamp()
        diagnostic.remarks = json.dumps(remark)
        diagnostic.save()
    else:
        diagnostic = MongoDiagnostics(service=service)
        diagnostic.remarks = remark
        diagnostic.save()
    return diagnostic.id
