import os
import json
import logging
from form_checker.utils.aws import (
    get_presigned_url,
    retrieve_bucket_info,
)
from form_checker.invoke import run


def handler(event, _):
    logging.info("Received event:", event)
    try:
        event = json.loads(event["body"])
    except:
        logging.warning("event is not stringified json:", event)

    bucket, key = retrieve_bucket_info(event)
    try:
        return run(
            get_presigned_url(bucket, key), upload=True, key=key, bucket=bucket
        )
    except Exception as e:
        logging.error(e)
        _, message = e.args
        return message
