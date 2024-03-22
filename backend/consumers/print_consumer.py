from confluent_kafka import Consumer, KafkaError

from obeilerding.consumers import abs_consumer


class PrintConsumer(abs_consumer.ObeilerdingConsumer):
    def __init__(self, server, security_protocol, mechanisms, username, password, group_id, auto_offset_reset, topic):
        super().__init__(server, security_protocol, mechanisms, username, password, group_id, auto_offset_reset, topic)

    def run(self):
        self.consumer = Consumer(**self.consumer_conf)
        self.consumer.subscribe([self.topic])

        while True:
            msg = self.consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    continue
                else:
                    print(msg.error())
                    break

            print(f"Received message: {msg.value().decode('utf-8')}")