import os
import boto3
import logging
from typing import TypedDict
from botocore.config import Config
from form_checker.utils.general import ProgressPercentage


class EventBucketInfo(TypedDict):
    bucket: int
    key: str


AWS_ACCESS_KEY = os.getenv("FC_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("FC_SECRET_ACCESS_KEY")

my_config = Config(
    s3={"addressing_style": "virtual"}
)  # , signature_version="v4")

s3_client = boto3.client(
    "s3",
    config=my_config,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

ses_client = boto3.client(
    "ses",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
}


def get_presigned_url(bucket: str, key: str):
    return s3_client.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
    )


def retrieve_bucket_info(event: dict) -> EventBucketInfo:
    s3 = event["Records"][0]["s3"]
    bucket = s3["bucket"]["name"]
    key = s3["object"]["key"]
    return {"bucket": bucket, "key": key}


def upload_file(file_path: str, bucket: str, key: str, extraArgs={}) -> str:
    logging.info(f"Uploading local file {file_path} to s3: {bucket}/{key}")
    try:
        s3_client.upload_file(
            file_path,
            bucket,
            key,
            ExtraArgs={"Metadata": {"source_path": file_path}, **extraArgs},
            Callback=ProgressPercentage(file_path),
        )
        try:
            os.remove(file_path)
        except:
            logging.warn(f"Failed removing file: {file_path}")
    except:
        raise
    logging.info("Successfully uploaded file to S3.")
    return key
