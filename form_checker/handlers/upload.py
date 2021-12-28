import json


def handler(event, context):
    response = {}
    response["statusCode"] = 302
    response["headers"] = {"Location": "https://nomenclate.readme.io/"}
    response["body"] = json.dumps({})
    return response
