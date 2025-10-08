import unittest
import uuid
import json
from sending_emails.core.rabitmq_publisher import get_rabbit_mq_publisher


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super(UUIDEncoder, self).default(obj)


class TestRabbitMQPublisher(unittest.TestCase):
    def test_publish_message(self):
        publisher = get_rabbit_mq_publisher()
        if publisher.connection_success:
            doc_payload = {
                "event": "collubi_paypal_send_mail",
                "message": "my name is shakeeb"
            }
            # Publish data to fastapi service
            encoded_message = json.dumps(doc_payload, cls=UUIDEncoder).encode("utf-8")
            publisher.publish_message(encoded_message, ttl=5000)
            if not publisher.publish_status:
                print("Test case failed to publish")
                self.assertEqual(False, publisher.publish_status)

            else:
                print("Test case successfully publish")
                self.assertEqual(True, publisher.publish_status)
            


if __name__ == '__main__':
    unittest.main()
