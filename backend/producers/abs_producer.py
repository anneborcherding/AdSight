import threading


class ObeilerdingProducer(threading.Thread):
    server: str = ""
    security_protocol: str = ""
    mechanisms: str = ""
    username: str = ""
    password: str = ""

    def __init__(self, server, security_protocol, mechanisms, username, password):
        super().__init__()

        self.server = server
        self.security_protocol = security_protocol
        self.mechanisms = mechanisms
        self.username = username
        self.password = password

    def run(self):
        raise NotImplementedError()