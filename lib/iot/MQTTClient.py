import logging
import paho.mqtt.client as mqtt

from .IOTClient import IOTClient

logger = logging.getLogger(__name__)

class MQTTClient(IOTClient):
    def __init__(self, broker_ip, port=1883) -> None:
        self.broker_ip = broker_ip
        self.port = port
        self.client = mqtt.Client() #create new instance
        self.client.connect_async(broker_ip, port)

        self.client.on_connect = self._on_connect
        self.client.on_connect_fail = self._on_connect_fail
        self.client.on_disconnect = self._on_disconnect

    def _on_disconnect(self):
        msg = f"Disconnected from {self.broker_ip}"
        logger.critical(msg)
        raise ConnectionError(msg)

    def _on_connect_fail(self):
        msg = f"Failed to connect to {self.broker_ip} @ port {self.port}"
        logger.critical(msg)
        raise ConnectionRefusedError(msg)

    def _on_connect(self):
        logger.info(f"Connected to {self.broker_ip} @ port {self.port}")

    def publish(self, topic, msg):
        return self.client.publish(topic, msg)

    def subscribe(self, topic):
        return self.client.subscribe(topic)