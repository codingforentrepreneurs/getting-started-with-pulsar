import json
import random
import sys

import pulsar


def produce(msg="hello world", count=2, topic="cfe-tenant/example-namespace/input-topic"):
    client = pulsar.Client('pulsar://localhost:6650')
    producer = client.create_producer(topic)
    for i in range(count):
        data = {"msg": f'{msg}-{(i+1) * random.randint(300, 20_200)}'}
        json_data = json.dumps(data)
        producer.send((json_data).encode('utf-8'))
    client.close()


if __name__ == "__main__":
    topic = "cfe-tenant/example-namespace/input-topic"
    args = sys.argv
    if len(args) > 1:
        topic = args[1]
    produce(msg="hello world", count=2, topic=topic)
