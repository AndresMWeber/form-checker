import os
import json
import logging
from form_checker.utils.aws import (
    cors_headers,
    get_presigned_url,
    retrieve_bucket_info,
    upload_file,
)
from form_checker.main import process


def handler(event, context):
    logging.info("Received event:", event)
    try:
        event = json.loads(event["body"])
    except:
        logging.warning("event is not stringified json:", event)

    bucket, key = retrieve_bucket_info(event)
    try:
        file_path = process(get_presigned_url(bucket, key))
        upload_file(file_path, bucket, key.replace("uploads", "processed"))
        return {"headers": cors_headers, "statusCode": 201}
    except Exception as e:
        logging.error(e)
        message = f"Error getting object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function."
        logging.error(message)
        return {"statusCode": 500, "message": message}
