from form_checker.utils.general import get_project_attribute
try:
    from form_checker.utils.aws import cors_headers
except ImportError:
    pass

def handler(event, context):
    response = {
        "headers": cors_headers,
        "statusCode": 200,
        "body": f"Welcome to Form Checker API version {get_project_attribute('tool','poetry','version')}!",
    }
    return response
