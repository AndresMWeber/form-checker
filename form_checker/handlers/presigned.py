import os
import logging
import json

try:
    from form_checker.utils.aws import s3_client, cors_headers
except ImportError:
    pass


def create_presigned_url(
    object_name, bucket_name=os.getenv("BUCKET"), expiration=120
):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    return s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket_name,
            "Key": f"uploads/{object_name}",
            "ContentType": "video/mp4",
        },
        ExpiresIn=expiration,
    )


def handler(event, context):
    try:
        body = json.loads(event["body"])
        response = {
            "headers": cors_headers,
            "statusCode": 201,
            "body": json.dumps({"url": create_presigned_url(body["filename"])}),
        }
        return response
    except Exception as e:
        logging.error(e)
        _, message = e.args
        return {"statusCode": 500, "message": message}
