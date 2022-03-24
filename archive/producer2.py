import pulsar

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('output-topic')

for i in range(2):
    producer.send(('hello-pulsar-%d' % i).encode('utf-8'))

client.close()
