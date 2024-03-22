from obeilerding.consumers import print_consumer, two_d_layout_consumer
from obeilerding.model import two_d_layout
from obeilerding.producers import retail_producer

KAFKA_BOOTSTRAP_SERVERS = 'SERVER:XXXX'
KAFKA_TOPIC = 'default'
KAFKA_USERNAME = 'USERNAME'
KAFKA_PASSWORD = 'THIS_IS_A_SECRET'
KAFKA_SECURITY_PROTOCOL = 'SASL_SSL'
KAFKA_MECHANISMS = 'SCRAM-SHA-512'
KAFKA_GROUP_ID = '1'
KAFKA_OFFSET_RESET = 'earliest'


def main():
    # Setup things

    # Define Producers and Consumers
    my_print_consumer = print_consumer.PrintConsumer(server=KAFKA_BOOTSTRAP_SERVERS,
                                                     security_protocol=KAFKA_SECURITY_PROTOCOL,
                                                     mechanisms=KAFKA_MECHANISMS, username=KAFKA_USERNAME,
                                                     password=KAFKA_PASSWORD, group_id=KAFKA_GROUP_ID,
                                                     auto_offset_reset=KAFKA_OFFSET_RESET, topic=KAFKA_TOPIC)

    my_layout_consumer = two_d_layout_consumer.TwoDLayoutConsumer(server=KAFKA_BOOTSTRAP_SERVERS,
                                                         security_protocol=KAFKA_SECURITY_PROTOCOL,
                                                         mechanisms=KAFKA_MECHANISMS, username=KAFKA_USERNAME,
                                                         password=KAFKA_PASSWORD, group_id=KAFKA_GROUP_ID,
                                                         auto_offset_reset=KAFKA_OFFSET_RESET, topic=KAFKA_TOPIC)
    consumers = [my_layout_consumer]

    my_retail_producer = retail_producer.RetailProducer(server=KAFKA_BOOTSTRAP_SERVERS,
                                                        security_protocol=KAFKA_SECURITY_PROTOCOL,
                                                        mechanisms=KAFKA_MECHANISMS, username=KAFKA_USERNAME,
                                                        password=KAFKA_PASSWORD, topic=KAFKA_TOPIC)

    producers = [my_retail_producer]

    # Run threads
    for producer in producers:
        producer.start()

    for consumer in consumers:
        consumer.start()


if __name__ == '__main__':
    main()
