import threading

from confluent_kafka import Consumer


class ObeilerdingConsumer(threading.Thread):
    server: str = ""
    security_protocol: str = ""
    mechanisms: str = ""
    username: str = ""
    password: str = ""
    group_id: str = ""
    auto_offset_reset: str = ""
    topic: str = ""
    consumer_conf: dict = {}
    consumer: Consumer = None

    def __init__(self, server: str, security_protocol: str, mechanisms: str, username: str, password: str, group_id: str, auto_offset_reset: str, topic: str):
        super().__init__()

        self.server = server
        self.security_protocol = security_protocol
        self.mechanisms = mechanisms
        self.username = username
        self.password = password
        self.group_id = group_id
        self.auto_offset_reset = auto_offset_reset
        self.topic = topic

        self.consumer_conf = {
            'bootstrap.servers': self.server,
            'security.protocol': self.security_protocol,
            'sasl.mechanisms': self.mechanisms,
            'sasl.username': self.username,
            'sasl.password': self.password,
            'group.id': self.group_id,
            'auto.offset.reset': self.auto_offset_reset
        }

    def run(self):
        raise NotImplementedError()
