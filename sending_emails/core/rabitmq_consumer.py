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
    send_otp_email,
    send_technician_credentials_create_by_hospital_admin_email,
    send_doctor_reviewer_credentials_create_by_hospital_admin_email,
    send_doctor_admin_credentials_create_by_hospital_admin_email,
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
        logger.info("AI Call Assistant Email Sending Consumer Service RabbitMQ Connection Channel: %s", rabbitmq_quee)
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

    # for otp sending email
    if event == "user_otp_request":
        data = user_payload.get("data")
        print("data is :::::::::::: \n ", data)
        send_otp_email(data=data)

    if event == "technician_create_by_hospital_admin":
        data = user_payload.get("data")
        print("data is :::::::::::: \n ", data)
        send_technician_credentials_create_by_hospital_admin_email(data=data)    

    if event == "doctor_reviewer_create_by_hospital_admin":
        data = user_payload.get("data")
        print("data is :::::::::::: \n ", data)
        send_doctor_reviewer_credentials_create_by_hospital_admin_email(data=data)   

    if event == "doctor_admin_create_by_hospital_admin":
        data = user_payload.get("data")
        print("data is :::::::::::: \n ", data)
        send_doctor_admin_credentials_create_by_hospital_admin_email(data=data)   

    else:
        logger.info("Received invalid event: %s", event)
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