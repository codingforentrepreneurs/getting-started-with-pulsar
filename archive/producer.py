import json
import random

import pulsar


def produce(msg="hello world", count=2):
    client = pulsar.Client('pulsar://localhost:6650')
    producer = client.create_producer('my-topic')
    for i in range(count):
        data = {"msg": f'{msg}-{(i+1) * random.randint(300, 20_200)}'}
        json_data = json.dumps(data)
        producer.send((json_data).encode('utf-8'))
    client.close()


if __name__ == "__main__":
    topic = "my-topic"
    produce(msg="hello world", count=2)
