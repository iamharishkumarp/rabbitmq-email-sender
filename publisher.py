import pika
import json
from config import RABBITMQ_HOST

def publish_email(to, subject, message):
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        # Declaring the queue
        channel.queue_declare(queue='email_queue', durable=True)
        # Create message dictionary
        email_data = {
            'to': to,
            'subject': subject,
            'message': message
        }
        # Publish to queue
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=json.dumps(email_data),
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )
    except Exception as e:
        print("Error publishing to RabbitMQ:", e)
