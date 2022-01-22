import json
from form_checker.settings import Config
from form_checker.utils.aws import cors_headers, list_videos, compose_s3_url


def handler(event, context):
    videos = list_videos()
    print(videos)
    video_urls = [
        url["url"]
        for url in [
            compose_s3_url(Config.BUCKET, video["Key"]) for video in videos
        ]
    ]
    response = {
        "headers": cors_headers,
        "statusCode": 200,
        "body": json.dumps(video_urls),
    }
    return response
