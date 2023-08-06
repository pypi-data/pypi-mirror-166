from fastapi.responses import Response
from hautils.logger import logger
import json


def json_response(content, status=200, pop_fields=list()):
    if content is None:
        logger.warn("json response object not found")
        return Response(content='{"message" : "object not found"}', status_code=status, media_type="application/json")

    response_object = json.loads(content.to_json())
    response_object["id"] = str(content.id)
    response_object.pop("_id")
    for field in pop_fields:
        response_object.pop(field)
    response = json.dumps(response_object)
    logger.info("json encode %s" % (response,))
    return Response(content=response, status_code=status, media_type="application/json")
