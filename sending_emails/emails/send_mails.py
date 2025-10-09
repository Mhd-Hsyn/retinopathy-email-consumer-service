import os
import ssl
import smtplib
from decouple import config
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sending_emails.emails.config import (
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST,
    EMAIL_PORT
)
import logging
logger = logging.getLogger("collubi_email_service_logger")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))





def send_otp(
        user_email: str,
        user_fullname: str,
        otp_reason: str,
        otp_expiry_time:str,
        new_otp_request_time:str,
        otp_request_at: str,
        otp: str,
):
    
    current_year = str(datetime.now().year)
    company_name = config('COMPANY_NAME')

    sender_email = EMAIL_HOST_USER

    message = MIMEMultipart("alternative")
    message["Subject"] = f"{otp_reason}"
    message["From"] = sender_email
    message["To"] = user_email

    # Path to the email template
    template_path = "sending_emails/emails/template/send_otp.html"
    logger.info ("template_path ================ %s", template_path)

    # Open and read the template HTML file
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_content = template_file.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("[user_fullname]", user_fullname)
    html_content = html_content.replace("[otp_reason]", otp_reason)
    html_content = html_content.replace("[otp]", otp)
    html_content = html_content.replace("[otp_expiry_time]", otp_expiry_time)
    html_content = html_content.replace("[otp_request_at]", otp_request_at)
    html_content = html_content.replace("[new_otp_request_time]", new_otp_request_time)
    html_content = html_content.replace("[current_year]", current_year)
    html_content = html_content.replace("[company_name]", company_name)
    

    # Create the plain-text and HTML version of your message

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
        server.login(sender_email, EMAIL_HOST_PASSWORD)

        server.sendmail(
            sender_email, user_email, message.as_string()
        )

    logger.info ("Email Send Successfully . . . ")
    return True



