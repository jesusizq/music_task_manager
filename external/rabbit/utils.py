import os
from .rabbitmq_client import RabbitMQClient


def send_job(job_data, queue_name):
    rabbit_client = RabbitMQClient(
        host=os.environ["RABBITMQ_BROKER"],
        port=os.environ["RABBITMQ_PORT"],
        queue=queue_name,
    )

    rabbit_client.publish(job_data)
    rabbit_client.close()
