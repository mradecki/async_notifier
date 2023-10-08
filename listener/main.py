import pika
import uuid

RABBITMQ_HOST = 'rabbitmq'  # Name of the RabbitMQ service in Docker Compose
EXCHANGE_NAME = 'exchange'  # Update with your exchange name
ROUTING_KEY = 'routing_key'  # Update with your routing key
QUEUE_NAME = str(uuid.uuid4())

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')
    channel.queue_declare(queue=QUEUE_NAME)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    print(f"Listening for messages from exchange '{EXCHANGE_NAME}' with routing key '{ROUTING_KEY}' on queue '{QUEUE_NAME}'. To exit, press CTRL+C")

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
