FROM apachepulsar/pulsar:2.9.1

COPY ./example_functions  /pulsar/example_functions

CMD [ "bin/pulsar", "standalone" ]