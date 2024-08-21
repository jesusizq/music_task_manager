import os
import pika
import json
import time


class RabbitMQClient:
    def __init__(
        self,
        host="localhost",
        port=5672,
        queue="task_queue",
        max_retries=5,
        retry_delay=5,
    ):
        self.host = host
        self.port = port
        self.queue = queue
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        credentials = pika.PlainCredentials(
            os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASSWORD"]
        )

        attempt = 0
        while attempt < self.max_retries:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.host, port=self.port, credentials=credentials
                    )
                )
                break
            except Exception as e:
                attempt += 1
                print(
                    f"Connection to RabbitMQ failed, trying again in {self.retry_delay} seconds ({attempt}/{self.max_retries})..."
                )
                time.sleep(self.retry_delay)
        else:
            raise ConnectionError(
                "Failed to connect to RabbitMQ after {self.max_retries} attempts."
            )

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def publish(self, message):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent, headers={}
            ),
        )

    def consume(self, callback):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
