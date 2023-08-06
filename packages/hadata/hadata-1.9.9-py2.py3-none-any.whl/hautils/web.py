from fastapi.responses import Response
import json


def json_response(content, status=200):
    response_object = json.loads(content.to_json())
    response_object["id"] = str(content.id)
    response_object.pop("_id")
    return Response(content=json.dumps(response_object), status_code=status, media_type="application/json")
