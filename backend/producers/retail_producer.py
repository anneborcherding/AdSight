import json
import os
import socket

import requests
from confluent_kafka import Producer

from obeilerding.producers import abs_producer
from utils.api import get_api_key_and_auth

from obeilerding.utils.api import DEVICE_UPDATE, DEVICE_ENTRY, DEVICE_EXIT


class RetailProducer(abs_producer.ObeilerdingProducer):
    api_key: str
    s: socket
    producer: Producer
    topic: str

    def __init__(self, server: str, security_protocol: str, mechanisms: str, username: str, password: str, topic: str):
        super().__init__(server, security_protocol, mechanisms, username, password)
        self.topic = topic

    def setup(self):

        # work around to get IP address on hosts with non resolvable hostnames
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.connect(("8.8.8.8", 80))
        IP_ADRRESS = self.s.getsockname()[0]
        self.s.close()
        url = 'http://' + str(IP_ADRRESS) + '/update/'

        # Tests to see if we already have an API Key
        try:
            if os.stat("../API_KEY.txt").st_size > 0:
                # If we do, lets use it
                f = open("../API_KEY.txt")
                self.apiKey = f.read()
                f.close()
            else:
                # If not, lets get user to create one
                self.apiKey = get_api_key_and_auth()
        except:
            self.apiKey = get_api_key_and_auth()

    def produce(self):

        # Opens a new HTTP session that we can use to terminate firehose onto
        s = requests.Session()
        s.headers = {'X-API-Key': self.apiKey}
        r = s.get(
            'https://partners.dnaspaces.io/api/partners/v1/firehose/events',
            stream=True)  # Change this to .io if needed

        # Jumps through every new event we have through firehose
        print("Starting Stream")
        for line in r.iter_lines():
            if line:
                # decodes payload into useable format
                decoded_line = line.decode('utf-8')
                event = json.loads(decoded_line)

                if event['eventType'] == DEVICE_UPDATE or event['eventType'] == DEVICE_ENTRY or event['eventType'] == DEVICE_EXIT:
                    try:
                        self.producer.produce(self.topic, json.dumps(event).encode('utf-8'))
                        self.producer.flush()
                    except Exception as e:
                        print(f"Error producing message: {e}")

                    # gets the event type out the JSON event and prints to screen
                    eventType = event['eventType']
                    print(eventType)

    def run(self):
        producer_conf = {
            'bootstrap.servers': self.server,
            'security.protocol': self.security_protocol,
            'sasl.mechanisms': self.mechanisms,
            'sasl.username': self.username,
            'sasl.password': self.password,
        }

        self.producer = Producer(**producer_conf)

        self.setup()

        self.produce()
