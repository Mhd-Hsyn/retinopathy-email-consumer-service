import json
import time
import logging
import pika
from sending_emails.core.config import (
    rabbitmq_username,
    rabbitmq_password,
    rabbitmq_host,
    rabbitmq_port,
    rabbitmq_quee,
    rabbitmq_exchange,
    rabbitmq_routing_key,
)
from sending_emails.emails.send_mails import (
    send_otp,
    send_welcome_email_law_firm_account_create,
    send_subscription_payment_sucessfull,
    send_welcome_email_lawyer_account_create,
    send_welcome_email_client_account_create,
    send_assigned_task_email,

)



logger = logging.getLogger("ai_call_assistant_saas_email_service_logger")
SUCCESS = True
FAILURE = False


def continous_consuming_rabitmq_messages(loop_behavior:str)->None:
    """Consume messages from a RabbitMQ queue and process them based on the user's role"""
    sleep_time = 10
    try:
        credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                rabbitmq_host, rabbitmq_port, "/", credentials
            )
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange=rabbitmq_exchange, exchange_type="direct"
        )
        channel.queue_declare(queue=rabbitmq_quee)
        channel.queue_bind(
            exchange=rabbitmq_exchange,
            queue=rabbitmq_quee,
            routing_key=rabbitmq_routing_key,
        )
        logger.info("Law Firm Email Sending Consumer Service RabbitMQ Connection Channel: %s", rabbitmq_quee)
        channel.basic_consume(
            queue=rabbitmq_quee,
            on_message_callback=rabitmq_consumer_callback,
            auto_ack=False,
        )
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as rabitmq_exception:
        logger.info("Connection error. Retrying in 5 seconds...")
        time.sleep(sleep_time)
        if loop_behavior != "1":
            continous_consuming_rabitmq_messages(loop_behavior)
    except Exception as swr:
        logger.info("An error occurred: %s", swr)
        time.sleep(sleep_time)
        if loop_behavior != "1":
            continous_consuming_rabitmq_messages(loop_behavior)



def rabitmq_consumer_callback(ch, method, properties, body)->bool:
    # ch.basic_ack(delivery_tag=method.delivery_tag)


    message = body.decode()
    user_payload = json.loads(message)
    print("user_payload=====>",user_payload)
    logging.info("********* user_payload ------ >>>>  %s",user_payload)

    event = user_payload.get("event")
    if not event == "lawfirm_crm_send_mail":
        logger.info("Received invalid event: %s", event)
        return FAILURE
    email_type = user_payload.get("email_type")
    print("\n\n ****** email_type _________________ ", email_type)

    # for otp sending email
    if email_type == "user_otp_request":
        data = user_payload.get("data")
        print("data is :::::::::::: \n ", data)
        print("email_type is :::::::::::: \n ", email_type)
        send_otp(
            user_email= data.get("user_email"),
            user_fullname= data.get("user_fullname"),
            otp_reason= data.get("otp_reason"),
            otp_expiry_time= data.get("otp_expiry_time"),
            new_otp_request_time= data.get("new_otp_request_time"),
            otp_request_at = data.get("otp_request_at"),
            otp= data.get("otp"),
        )
    
    # for Law-Firm new acount created send credentials
    elif email_type == "lawfirm_account_created":
        data = user_payload.get("data")
        send_welcome_email_law_firm_account_create(
            data = data,
            email = data['email'],
        )

    elif email_type == "subscription_payment_sucessfull":
        data = user_payload.get("data")
        send_subscription_payment_sucessfull(
            data = data,
            email = data['email'],
        )
    
    # for lawyer new acount created send credentials
    elif email_type == "lawyer_account_created":
        data = user_payload.get('data')
        send_welcome_email_lawyer_account_create(
            email= data['email'],
            data= data
        )

    # for lawyer new acount created send credentials
    elif email_type == "client_account_created":
        data = user_payload.get('data')
        send_welcome_email_client_account_create(
            email= data['email'],
            data= data
        )

    elif email_type == "assigned_task_notification":
        data = user_payload.get("data")
        send_assigned_task_email(
            email=data['email'],
            data=data
        )
        
        

    else:
        logger.info("Received unknown email type: %s", email_type)
        return FAILURE

    logger.info("Processed message: %s", message)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return SUCCESS
    


def consume_messages(loop_behavior:str="infinite_running")->None:
    """Continously run rabitmq consumer"""
    while True:
        if loop_behavior != "1":
            continous_consuming_rabitmq_messages(loop_behavior)
        else:
            continous_consuming_rabitmq_messages(loop_behavior)
            break