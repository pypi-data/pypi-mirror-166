from fastapi.responses import Response


def json_response(content, status=200):
    return Response(content=content.to_json(), status_code=status, media_type="application/json")
