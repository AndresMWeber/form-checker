import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

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
