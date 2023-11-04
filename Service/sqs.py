from botocore.exceptions import ClientError
import json
import boto3

class SQS:
    def __init__(self, logger):
        self.logger = logger
        session = boto3.session.Session()
        self.sqs = session.client(
            service_name='sqs',
            endpoint_url='https://sqs.eu-central-1.amazonaws.com/',
        )
    
    def get_queue_url_by_name(self, name):
        try:
            queue = self.sqs.get_queue_url(QueueName=name)
            self.logger.info(f"Got queue {name} with URL={queue['QueueUrl']}")
            return queue['QueueUrl']
        except ClientError as error:
            self.logger.exception(f"Couldn't get queue named {name}.")
            raise error
    
    def send_message(self,queue_name, message_body, message_attributes=None):
        if not message_attributes:
            message_attributes = {}

        try:
            queue_url = self.get_queue_url_by_name(queue_name)
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body,
                MessageAttributes=message_attributes
            )
            self.logger.info(f"Message Sent to Queue: {queue_name} and the message id: {response['MessageId']}")
            return response
        except ClientError as error:
            self.logger.exception("Send message failed: %s", message_body)
            raise error