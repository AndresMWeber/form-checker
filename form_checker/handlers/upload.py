import json
import logging
from form_checker.utils.aws import (
    get_presigned_url,
    retrieve_bucket_info,
)
from form_checker.main import run


def handler(event, _):
    logging.info("Received event:", event)
    try:
        event = json.loads(event["body"])
    except:
        logging.warning("event is not stringified json:", event)

    bucket, key = retrieve_bucket_info(event)
    try:
        run(
            get_presigned_url(bucket, key), upload=True, key=key, bucket=bucket
        )
        logging.info("Finished processing video successfully.")
    except Exception as e:
        logging.error(e)
        message = f"Error processing object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function."
        logging.error(message)
