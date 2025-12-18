import os
from decouple import config
from datetime import datetime
from typing import Dict
import logging
from sending_emails.emails.encryption_utils import decrypt_data
from .helpers import (
    render_template,
    send_email
)

logger = logging.getLogger("ai_call_assistant_service_logger")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPANY_NAME = config("COMPANY_NAME")
COMPANY_LOGO = config("COMPANY_LOGO")

TEMPLATE_FOLDER_PATH="sending_emails/emails/template"



def send_otp_email(data: Dict[str, str]) -> bool:
    """Send OTP verification email."""
    template = f"{TEMPLATE_FOLDER_PATH}/send_otp.html"
    current_year = str(datetime.now().year)

    replacements = {
        "user_fullname": data.get("user_fullname"),
        "otp_reason": data.get("otp_reason"),
        "otp": decrypt_data(encrypted_data=data.get("otp")),
        "otp_expiry_time": data.get("otp_expiry_time"),
        "otp_request_at": data.get("otp_request_at"),
        "new_otp_request_time": data.get("new_otp_request_time"),
        "current_year": current_year,
        "company_name": COMPANY_NAME,
        "company_logo_url": COMPANY_LOGO,
        "dynamic_info_1": data.get("dynamic_info_1"),
        "dynamic_info_2": data.get("dynamic_info_2")
    }

    html_content = render_template(template, replacements)
    subject = data.get("otp_reason", "OTP Verification")
    return send_email(subject, data.get("user_email"), html_content)


def send_technician_credentials_create_by_hospital_admin_email(
    data: Dict[str, str]
) -> bool:
    """
    Send technician credentials email created by hospital admin
    """

    template = f"{TEMPLATE_FOLDER_PATH}/technician_credentials.html"
    current_year = str(datetime.now().year)

    replacements = {
        "user_fullname": data.get("user_fullname"),
        "user_email": data.get("user_email"),
        "hospital_name": data.get("hospital_name"),
        "account_created": data.get("account_created"),
        "password": decrypt_data(encrypted_data=data.get("password")),
        "current_year": current_year,
        "company_name": COMPANY_NAME,
        "company_logo_url": COMPANY_LOGO,
    }

    html_content = render_template(template, replacements)

    subject = "Your Technician Account Credentials"

    return send_email(
        subject=subject,
        recipient=data.get("user_email"),
        html_content=html_content
    )


def send_doctor_reviewer_credentials_create_by_hospital_admin_email(
    data: Dict[str, str]
) -> bool:
    """
    Send doctor credentials email created by hospital admin
    """

    template = f"{TEMPLATE_FOLDER_PATH}/doctor_reviewer_credentials.html"
    current_year = str(datetime.now().year)

    replacements = {
        "user_fullname": data.get("user_fullname"),
        "user_email": data.get("user_email"),
        "hospital_name": data.get("hospital_name"),
        "account_created": data.get("account_created"),
        "password": decrypt_data(encrypted_data=data.get("password")),
        "current_year": current_year,
        "company_name": COMPANY_NAME,
        "company_logo_url": COMPANY_LOGO,
    }

    html_content = render_template(template, replacements)

    subject = "Your Doctor Account Credentials"

    return send_email(
        subject=subject,
        recipient=data.get("user_email"),
        html_content=html_content
    )



