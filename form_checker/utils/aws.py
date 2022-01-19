import os
import boto3
import logging
from botocore.config import Config
from dotenv import load_dotenv
from form_checker.utils.general import ProgressPercentage

load_dotenv()
my_config = Config(
    s3={"addressing_style": "virtual"}
)  # , signature_version="v4")

s3_client = boto3.client(
    "s3",
    config=my_config,
    aws_access_key_id=os.getenv("AW_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AW_SECRET_ACCESS_KEY"),
)

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
}


def get_presigned_url(bucket, key):
    return s3_client.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
    )


def retrieve_bucket_info(event):
    s3 = event["Records"][0]["s3"]
    name = s3["bucket"]["name"]
    key = s3["object"]["key"]
    return (name, key)


def upload_file(file_path, bucket, key):
    logging.info(f"Uploading local file {file_path} to s3: {bucket}/{key}")
    try:
        s3_client.upload_file(
            file_path,
            bucket,
            key,
            ExtraArgs={"Metadata": {"source_path": file_path}},
            Callback=ProgressPercentage(file_path),
        )
        try:
            os.remove(file_path)
        except:
            logging.warn(f'Failed removing file: {file_path}')
    except:
        raise
    logging.info("Successfully uploaded file to S3.")
