import datetime

from hadata.meta import MongoDiagnostics


def get_diagnostic_record(service):
    return MongoDiagnostics.objects.filter(service=service)


def add_diagnostic_record(service, remark):
    diagnostic = MongoDiagnostics(service=service)
    diagnostic.timestamp = datetime.datetime.now().timestamp()
    diagnostic.remarks = remark
    diagnostic.save()
    return diagnostic.id