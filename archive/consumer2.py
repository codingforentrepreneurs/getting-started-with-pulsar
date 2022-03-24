import json

import pulsar

client = pulsar.Client('pulsar://localhost:6650')
consumer = client.subscribe('output-topic',
                            subscription_name='my-sub')

while True:
    msg = consumer.receive()
    data = msg.data()
    if isinstance(data, bytes):
        msg_txt = data.decode()
        # print("decoded", msg_txt, type(msg_txt))
        if isinstance(msg_txt, str):
            json_data = {}
            try:
                json_data = json.loads(msg_txt)
            except: 
                pass
            for k,v in json_data.items():
                print(k, v)
    # print("Received message: '%s'" % data)
    consumer.acknowledge(msg)
