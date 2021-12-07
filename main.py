"""
Style server service main
"""
import json
import os
import sys

import pika
import requests

from service import moss


def callback(channel, method, _, body):
    """
    Callback function for receiving message
    """
    body = json.loads(body)
    log = bool(os.getenv("LOG"))
    respath = os.getenv("SUBMISSION_URL")+"/code"
    backend_req = requests.post(respath, json=body)
    backend_res = json.loads(backend_req.text)
    result = moss.file_check(
        body["problem_id"], body["language"], backend_res["submission_list"]
    )
    path = os.getenv("CLASS_URL")+"/" + \
        body["class_id"]+"/problem/"+body["problem_id"]+"/moss"
    if log:
        print(path)
    res = requests.post(path, json={
        "url": result
    })
    if res.status_code == 200:
        print("[INFO] Moss result sent")
        if log:
            print(res.text)
    else:
        print("[ERROR] Moss result not sent")
        if log:
            print(res.text)
        sys.exit(0)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """
    Main function
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ"),
            credentials=pika.credentials.PlainCredentials(
                os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD")
            )
        )
    )
    channel = connection.channel()
    queue_name = "program_moss"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            print('Interrupted')
            sys.exit(0)
        except SystemExit:
            print('Interrupted')
            raise
