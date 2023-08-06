import traceback

from fastapi.responses import Response
from hautils.logger import logger
import json
from mongoengine import Document, QuerySet


def mongo_to_dict(content):
    if not issubclass(type(content), Document):
        logger.warn("json response object not found")
        raise Exception

    response_object = json.loads(content.to_json())
    response_object["id"] = str(content.id)
    response_object.pop("_id")
    return response_object


def json_response(content, status=200, pop_fields=list()):
    try:
        if issubclass(type(content), QuerySet):
            response = []
            for doc in content:
                d = mongo_to_dict(doc)
                for field in pop_fields:
                    d.pop(field)
                response.append(d)
        else:
            response = mongo_to_dict(content)
            for field in pop_fields:
                response.pop(field)
        response = json.dumps(response)
        logger.info("json encode %s" % (response,))
        return Response(content=response, status_code=status, media_type="application/json")
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exception(type(e), e, e.__traceback__))

    return Response(content='{"message" : "object not found"}', status_code=403, media_type="application/json")


def mongo_to_log(content):
    try:
        return json.dumps(mongo_to_dict(content))
    except Exception as e:
        return ""
