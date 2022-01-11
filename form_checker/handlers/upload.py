import os
import json
import logging
from form_checker.utils.aws import s3_client, cors_headers
from form_checker.utils.process_video import run
from form_checker.utils.general import ProgressPercentage


def retreive_bucket_info(event):
    s3 = event["Records"][0]["s3"]
    name = s3["bucket"]["name"]
    key = s3["object"]["key"]
    return (name, key)


def process_video(bucket, key):
    file_path = run(get_presigned_url(bucket, key))
    upload_video(file_path, bucket, key.replace("uploads", "processed"))


def get_presigned_url(bucket, key):
    return s3_client.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
    )


def upload_video(file_path, bucket, key):
    logging.info(f"Uploading local file {file_path} to s3: {bucket}/{key}")
    try:
        s3_client.upload_file(
            file_path,
            bucket,
            key,
            ExtraArgs={"Metadata": {"source_path": file_path}},
            Callback=ProgressPercentage(file_path),
        )
        os.remove(file_path)
    except:
        raise
    logging.info("Successfully uploaded file to S3.")


def handler(event, context):
    logging.info("Received event:", event)
    try:
        event = json.loads(event["body"])
    except:
        logging.warning("event is not stringified json:", event)
    # Get the object from the event and show its content type
    bucket, key = retreive_bucket_info(event)
    try:
        process_video(bucket, key)
        return {"headers": cors_headers, "statusCode": 201}
    except Exception as e:
        logging.error(e)
        message = f"Error getting object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function."
        logging.error(message)
        return {"statusCode": 500, "message": message}
