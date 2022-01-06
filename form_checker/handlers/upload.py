import logging
import json
import asyncio
from form_checker.utils.aws import s3_client
from form_checker.utils.process_video import run


def retreive_bucket_info(event):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    return (bucket, key)


async def process_video(bucket, key):
    file_url = s3_client.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
    )
    file_path = run(file_url)
    await s3_client.upload_file(
        file_path, bucket, key.replace("uploads", "processed")
    )


def handler(event, context):
    try:
        logging.info("Received event:", json.stringify(event, None, 2))
    except:
        logging.info("event is not json:")
        logging.info(event)
    # Get the object from the event and show its content type
    bucket, key = retreive_bucket_info(event)
    try:
        asyncio.get_event_loop().run_until_complete(process_video(bucket, key))
        return {"StatusCode": 201}
    except Exception as e:
        logging.error(e)
        message = f"Error getting object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function."
        logging.error(message)
        return {"StatusCode": 500, "message": message}
