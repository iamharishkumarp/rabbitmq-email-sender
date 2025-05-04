import pika
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# SMTP settings
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

# RabbitMQ connection settings
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

# Declare the queue (ensure it exists)
channel.queue_declare(queue='email_queue', durable=True)

print("[*] Waiting for messages. To exit press CTRL+C")

# Function to send an email using SMTP
def send_email_via_smtp(to_email, subject, message):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Set up the SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())  # Send the email
        server.quit()  # Disconnect from the server

        print(f"Email sent to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Define the callback to handle messages
def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[x] Received message: {data}")

    # Get the email details from the message
    to_email = data['to']
    subject = data['subject']
    message = data['message']

    # Send the email via SMTP
    send_email_via_smtp(to_email, subject, message)

    # Acknowledge message processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming
channel.basic_consume(queue='email_queue', on_message_callback=callback)

# Blocking call — keeps the consumer running
channel.start_consuming()




