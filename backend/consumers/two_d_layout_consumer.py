import json

from confluent_kafka import Consumer, KafkaError

from obeilerding.consumers import abs_consumer
from obeilerding.model.two_d_layout import TwoDLayout
from obeilerding.utils.api import DEVICE_UPDATE, DEVICE_EXIT, DEVICE_ENTRY


class TwoDLayoutConsumer(abs_consumer.ObeilerdingConsumer):
    twoDLayout = TwoDLayout()

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
            content = json.loads(msg.value().decode('utf-8'))

            if content['eventType'] == DEVICE_UPDATE:
                mac_address = content['deviceLocationUpdate']['device']['macAddress']
                x_pos = content['deviceLocationUpdate']['xPos']
                y_pos = content['deviceLocationUpdate']['yPos']
                if 'floorNumber' in content['deviceLocationUpdate']['location']['parent'].keys():
                    floor = content['deviceLocationUpdate']['location']['parent']['floorNumber']
                else:
                    floor = -1
                self.twoDLayout.location_update(mac_address, x_pos, y_pos, floor)

            elif content['eventType'] == DEVICE_ENTRY:
                mac_address = content['devicePresence']['device']['macAddress']
                self.twoDLayout.device_entry(mac_address)

            elif content['eventType'] == DEVICE_EXIT:
                mac_address = content['devicePresence']['device']['macAddress']
                self.twoDLayout.device_exit(mac_address)
            else:
                pass
