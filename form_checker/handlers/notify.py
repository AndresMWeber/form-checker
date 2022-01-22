import logging
import os
from form_checker.settings import Config
from form_checker.utils.aws import retrieve_bucket_info,compose_s3_url
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def handler(event, _):
    bucket_data = retrieve_bucket_info(event)
    s3_urls = compose_s3_url(bucket_data['bucket'], bucket_data['key'])
    s3_path = s3_urls['path']
    s3_url = s3_urls['url']
    subject = "New video uploaded to {s3_path}"
    recipient = Config.EMAIL_DESTINATION
    sender = Config.EMAIL_SOURCE
    message = f"A new video was uploaded to {s3_path} at {s3_url}"
    message_html = (
        f'A new video was uploaded to <a href="{s3_url}">{s3_path}</a>'
    )

    logging.info(f"Sending email from {sender} to {recipient} - {message}")

    if not Config.EMAIL_DESTINATION:
        raise IOError(
            "Must supply an email address to send to via a Lambda/Local environment variable FC_EMAIL_DESTINATION"
        )

    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        plain_text_content=message,
        html_content=message_html,
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        logging.info(f"Successfully sent email: {response}")
        return response
    except Exception as e:
        _, message = e.args
        logging.error(message)
        return e
