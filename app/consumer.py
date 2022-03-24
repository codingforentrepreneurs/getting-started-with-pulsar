import json
import sys

import pulsar


def consumer(topic="cfe-tenant/example-namespace/input-topic", subscription_name='my-sub'):
    client = pulsar.Client('pulsar://localhost:6650')
    consumer = client.subscribe(topic, subscription_name=subscription_name)
    while True:
        msg = consumer.receive()
        data = msg.data()
        if isinstance(data, bytes):
            msg_txt = data.decode()
            if isinstance(msg_txt, str):
                json_data = {}
                try:
                    json_data = json.loads(msg_txt)
                except Exception as e: 
                    json_data = msg_txt
                if isinstance(json_data, str):
                    print("txt data:", json_data)
                if isinstance(json_data, dict):
                    for k,v in json_data.items():
                        print("key:", k, "value:", v)
        consumer.acknowledge(msg)
    client.close()


if __name__ == "__main__":
    topic="cfe-tenant/example-namespace/input-topic"
    args = sys.argv
    if len(args) > 1:
        topic = args[1]
    consumer(topic=topic)
