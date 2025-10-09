import os
import ssl
import smtplib
from typing import Optional, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sending_emails.emails.config import (
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST,
    EMAIL_PORT
)
import logging
logger = logging.getLogger("ai_call_assistant_service_logger")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def safe_replace(content: str, tag: str, value: Optional[str], default="N/A") -> str:
    """Safely replace a tag with value (or default if None)."""
    return content.replace(tag, str(value) if value else default)


def read_template(template_path: str) -> str:
    """Read and return the HTML email template content."""
    if not os.path.exists(template_path):
        logger.error(f"Template not found: {template_path}")
        raise FileNotFoundError(f"Template not found at {template_path}")
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def render_template(template_path: str, replacements: Dict[str, str]) -> str:
    """Render template by replacing placeholders with actual values."""
    html = read_template(template_path)
    for key, value in replacements.items():
        html = safe_replace(html, f"[{key}]", value)
    return html


def send_email(subject: str, recipient: str, html_content: str) -> bool:
    """Send an HTML email using SMTP over SSL."""
    sender_email = EMAIL_HOST_USER

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient

    part = MIMEText(html_content, "html")
    msg.attach(part)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
            server.login(sender_email, EMAIL_HOST_PASSWORD)
            server.sendmail(sender_email, recipient, msg.as_string())
        logger.info(f"✅ Email sent successfully to {recipient}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
        return False

