"""This module contains the main FastAPI application"""
import threading
import logging
import uvicorn
from fastapi import FastAPI
from sending_emails.core.rabitmq_consumer import consume_messages


app = FastAPI()
# Creating logger
dev_logger = logging.getLogger("ai_call_assistant_saas_email_service_logger")
dev_logger.setLevel(logging.INFO)
# Create a handler and associate the formatter with it
formatter = logging.Formatter(
    "%(asctime)s  | %(levelname)s | %(filename)s | %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
dev_logger.addHandler(handler)
logger = logging.getLogger("ai_call_assistant_saas_email_service_logger")


# Create a separate thread for message consumption
consumer_thread = threading.Thread(target=consume_messages, daemon=True)
consumer_thread.start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8009, reload=True)