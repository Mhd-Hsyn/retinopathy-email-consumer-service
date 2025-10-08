from cryptography.fernet import Fernet
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



def decrypt_text(encrypted_password: str) -> str:
    """
    Decrypts an encrypted password back to plain text.
    """
    fernet = Fernet(config('ENCRYPTION_SECRET_KEY').encode())
    return fernet.decrypt(encrypted_password.encode()).decode()




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




def send_welcome_email_law_firm_account_create(
    email: str,
    data : dict
):
    
    current_year = str(datetime.now().year)
    company_name = config('COMPANY_NAME')
    company_logo = config('COMPANY_LOGO')
    login_url = config('LOGIN_URL')

    sender_email = EMAIL_HOST_USER
    
    full_name = data['full_name']

    message = MIMEMultipart("alternative")
    message["Subject"] = f"{full_name} Your Firm Account created sucessfully"
    message["From"] = sender_email
    message["To"] = email

    # Path to the email template
    template_path = "sending_emails/emails/template/firm_account_created_welcome.html"
    logger.info ("template_path ================ %s", template_path)


    # Open and read the template HTML file
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_content = template_file.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("[full_name]", data['full_name'])
    html_content = html_content.replace("[email]", data['email'])
    html_content = html_content.replace("[mobile_number]", data['mobile_number'])
    html_content = html_content.replace("[password]", data.get('password', ""))
    # html_content = html_content.replace("[profile_image]", data['profile_image'])
    html_content = html_content.replace("[profile_image]", company_logo)
    html_content = html_content.replace("[login_url]", login_url)

    part2 = MIMEText(html_content, "html")
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
        server.login(sender_email, EMAIL_HOST_PASSWORD)

        server.sendmail(
            sender_email, email, message.as_string()
        )

    logger.info ("Email Send Successfully . . . ")
    return True


def send_subscription_payment_sucessfull(
    email: str,
    data : dict
):
    
    current_year = str(datetime.now().year)
    company_name = config('COMPANY_NAME')
    sender_email = EMAIL_HOST_USER
    package_name = data['package_detail']['name']
    payment_amount = data['payment_detail']['amount']

    email_subject = f"Payment of ${payment_amount} Received – Your Subscription {package_name} plan"

    # Path to the email template
    template_path = "sending_emails/emails/template/subscription_payment_sucessfull.html"
    logger.info ("template_path ================ %s", template_path)


    # Dynamic heading based on subscription status
    if data["status"].lower() in ["trialing", "Trialing"]:
        template_path = "sending_emails/emails/template/subscription_trial_sucessfull.html"
        email_subject = f"Free 7-Day Trial Activated for Your Firm – {package_name} Plan"

    # Open and read the template HTML file
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_content = template_file.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("[full_name]", data['full_name'])

    # Subscription details 
    html_content = html_content.replace("[stripe_subscription_id]", data["stripe_subscription_id"])
    html_content = html_content.replace("[stripe_customer_id]", data["stripe_customer_id"])
    html_content = html_content.replace("[expiration_date]", data["expiration_date"])
    html_content = html_content.replace("[subscription_status]", data["status"])
    html_content = html_content.replace("[subscription_type]", data["subscription_type"])
    html_content = html_content.replace("[created_at]", data["created_at"])

    # Package details
    html_content = html_content.replace("[package_name]", data["package_detail"]["name"])
    html_content = html_content.replace("[package_duration]", data["package_detail"]["package_duration"])
    html_content = html_content.replace("[no_of_lawyers]", str(data["package_detail"]["no_of_lawyers"]))
    html_content = html_content.replace("[no_of_case_per_lawyer]", str(data["package_detail"]["no_of_case_per_lawyer"]))
    html_content = html_content.replace("[base_cost_per_lawyer]", data["package_detail"]["base_cost_per_lawyer"])
    html_content = html_content.replace("[base_cost_per_case]", data["package_detail"]["base_cost_per_case"])

    # Payment details
    html_content = html_content.replace("[transaction_id]", str(data["payment_detail"]["transaction_id"]))
    html_content = html_content.replace("[invoice_id]", data["payment_detail"]["invoice_id"])
    html_content = html_content.replace("[invoice_number]", data["payment_detail"]["invoice_number"])
    html_content = html_content.replace("[amount]", data["payment_detail"]["amount"])
    html_content = html_content.replace("[currency]", data["payment_detail"]["currency"])
    html_content = html_content.replace("[payment_status]", data["payment_detail"]["status"])
    html_content = html_content.replace("[hosted_invoice_url]", data["payment_detail"]["hosted_invoice_url"])
    html_content = html_content.replace("[invoice_pdf]", data["payment_detail"]["invoice_pdf"])

    html_content = html_content.replace("[current_year]", current_year)
    html_content = html_content.replace("[company_name]",  company_name)


    message = MIMEMultipart("alternative")
    message["Subject"] = email_subject
    message["From"] = sender_email
    message["To"] = email

    part2 = MIMEText(html_content, "html")
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
        server.login(sender_email, EMAIL_HOST_PASSWORD)

        server.sendmail(
            sender_email, email, message.as_string()
        )

    logger.info ("Email Send Successfully . . . ")
    print("EMAIL SEND SUCESSFULLY ___________________ \n\n, for subscription_payment_sucessfull \n\n")
    return True




def send_welcome_email_lawyer_account_create(
    email: str,
    data : dict
):
    
    current_year = str(datetime.now().year)
    company_name = config('COMPANY_NAME')
    company_logo = config('COMPANY_LOGO')
    login_url = config('LOGIN_URL')

    sender_email = EMAIL_HOST_USER
    
    full_name = data['full_name']
    firm_name = data['firm_name']

    message = MIMEMultipart("alternative")
    message["Subject"] = f"{full_name} Your Lawyer Account created with {firm_name} Firm"
    message["From"] = sender_email
    message["To"] = email

    # Path to the email template
    template_path = "sending_emails/emails/template/lawyer_account_created_welcome.html"
    logger.info ("template_path ================ %s", template_path)


    # Open and read the template HTML file
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_content = template_file.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("[full_name]", data.get("full_name", ""))
    html_content = html_content.replace("[first_name]", data.get("first_name", ""))
    html_content = html_content.replace("[last_name]", data.get("last_name", ""))
    html_content = html_content.replace("[email]", data.get("email", ""))
    html_content = html_content.replace("[mobile_number]", data.get("mobile_number") or "N/A")
    html_content = html_content.replace("[profile_image]", data.get("profile_image", ""))
    html_content = html_content.replace("[firm_name]", data.get("firm_name", ""))
    html_content = html_content.replace("[firm_user_fullname]", data.get("firm_user_fullname", ""))
    html_content = html_content.replace("[password]", data.get("password", ""))
    html_content = html_content.replace("[login_url]", login_url)
    html_content = html_content.replace("[current_year]", current_year)

    print(html_content)

    part2 = MIMEText(html_content, "html")
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
        server.login(sender_email, EMAIL_HOST_PASSWORD)

        server.sendmail(
            sender_email, email, message.as_string()
        )

    logger.info ("Email Send Successfully . . . ")
    return True



def send_welcome_email_client_account_create(
    email: str,
    data : dict
):
    print("************************** DATA ************************** \n\n ", data)
    
    current_year = str(datetime.now().year)
    company_name = config('COMPANY_NAME')
    company_logo = config('COMPANY_LOGO')
    login_url = config('LOGIN_URL')

    sender_email = EMAIL_HOST_USER
    
    full_name = ""
    firm_name = ""
    full_name = data['full_name']
    firm_name = data['firm_name']

    message = MIMEMultipart("alternative")
    message["Subject"] = f"{full_name} Your Lawyer Account created with {firm_name} Firm"
    message["From"] = sender_email
    message["To"] = email

    # Path to the email template
    template_path = "sending_emails/emails/template/client_account_created_welcome.html"
    logger.info ("template_path ================ %s", template_path)


    # Open and read the template HTML file
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_content = template_file.read()

    decrypted_password = decrypt_text(data.get("password", ""))

    # Replace placeholders with actual values
    html_content = html_content.replace("[full_name]", data.get("full_name", ""))
    html_content = html_content.replace("[first_name]", data.get("first_name", ""))
    html_content = html_content.replace("[last_name]", data.get("last_name", ""))
    html_content = html_content.replace("[email]", data.get("email", ""))
    html_content = html_content.replace("[mobile_number]", data.get("mobile_number") or "N/A")
    html_content = html_content.replace("[profile_image]", data.get("profile_image", ""))
    html_content = html_content.replace("[firm_name]", data.get("firm_name", ""))
    html_content = html_content.replace("[firm_user_fullname]", data.get("firm_user_fullname", ""))
    html_content = html_content.replace("[password]", decrypted_password)
    html_content = html_content.replace("[login_url]", login_url)
    html_content = html_content.replace("[current_year]", current_year)

    print(html_content)

    part2 = MIMEText(html_content, "html")
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
        server.login(sender_email, EMAIL_HOST_PASSWORD)

        server.sendmail(
            sender_email, email, message.as_string()
        )

    logger.info ("Email Send Successfully . . . ")
    return True


def send_assigned_task_email(email: str, data: dict):
    from datetime import datetime
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    current_year = str(datetime.now().year)
    sender_email = EMAIL_HOST_USER
    login_url = config("LOGIN_URL")  # Optional if needed in template
    company_logo = config("COMPANY_LOGO")
    firm_name = data.get("assigned_by_info", {}).get("name", "Your Law Firm")
    task_name = data['task_info']['title']
    matter_name = data['matter_info']['title']

    message = MIMEMultipart("alternative")
    message["Subject"] = f"New Task Assigned - {task_name} in matter {matter_name}"
    message["From"] = sender_email
    message["To"] = email

    template_path = "sending_emails/emails/template/lawyer_task_assigned_notification.html"

    with open(template_path, "r", encoding="utf-8") as template_file:
        html_content = template_file.read()

    # Replace placeholders
    html_content = html_content.replace("[lawyer_name]", data['lawyer_info']['name'])
    html_content = html_content.replace("[task_title]", data['task_info']['title'])
    html_content = html_content.replace("[task_description]", data['task_info']['description'])
    html_content = html_content.replace("[task_deadline]", data['task_info']['deadline'])
    html_content = html_content.replace("[task_priority]", data['task_info']['priority'])
    html_content = html_content.replace("[task_status]", data['task_info']['status'])
    html_content = html_content.replace("[task_type]", data['task_info']['type'])

    html_content = html_content.replace("[matter_title]", data['matter_info']['title'])
    html_content = html_content.replace("[matter_summary]", data['matter_info']['summary'])
    html_content = html_content.replace("[matter_priority]", data['matter_info']['priority'])
    html_content = html_content.replace("[matter_stage]", data['matter_info']['stage'])
    html_content = html_content.replace("[matter_start_date]", data['matter_info']['start_date'])
    html_content = html_content.replace("[matter_practice_area]", data['matter_info']['practicing_area'])

    html_content = html_content.replace("[client_name]", data['client_info']['full_name'])
    html_content = html_content.replace("[client_email]", data['client_info']['email'])
    html_content = html_content.replace("[client_phone]", data['client_info']['phone'])

    html_content = html_content.replace("[assigned_by_name]", data['assigned_by_info']['name'])
    html_content = html_content.replace("[assigned_by_email]", data['assigned_by_info']['email'])

    html_content = html_content.replace("[current_year]", current_year)

    part = MIMEText(html_content, "html")
    message.attach(part)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
        server.login(sender_email, EMAIL_HOST_PASSWORD)

        server.sendmail(
            sender_email, email, message.as_string()
        )

    logger.info ("Email Send Successfully . . . ")
    return True

