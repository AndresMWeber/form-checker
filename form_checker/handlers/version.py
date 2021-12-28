from form_checker.utils.general import get_project_attribute


def handler(event, context):
    response = {
        "statusCode": 200,
        "body": f"Welcome to Form Checker API version {get_project_attribute('tool','poetry','version')}!",
    }
    return response
