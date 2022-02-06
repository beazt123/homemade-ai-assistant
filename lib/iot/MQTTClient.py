import logging
import paho.mqtt.client as mqtt

from .IOTClient import IOTClient


class MQTTClient(IOTClient):
    logger = logging.getLogger(__name__)
    
    def __init__(self, chosen_commands, broker_ip, port=1883) -> None:
        MQTTClient.logger.info(f"MQTTBroker attempting to subscribe to {chosen_commands}")
        super().__init__(chosen_commands)
        self.broker_ip = broker_ip
        self.port = port
        self.client = mqtt.Client() #create new instance
        MQTTClient.logger.info(f"MQTTBroker attempting to connect to {broker_ip}:{port}")
        self.client.connect(broker_ip, port)
        MQTTClient.logger.info(f"MQTTBroker connected to {broker_ip}:{port}")


        # self.client.on_connect = self._on_connect
        self.client.on_connect_fail = self._on_connect_fail
        # self.client.on_disconnect = self._on_disconnect
        MQTTClient.logger.info(f"MQTTBroker callbacks set")
        self.client.loop_start()
        MQTTClient.logger.info(f"Started looping in background thread")

    def __del__(self):
        self.client.loop_stop(force=False)
        MQTTClient.logger.info(f"Stopped looping in background thread")

    def _on_disconnect(self, client, userdata, rc):
        msg = f"Disconnected from {self.broker_ip}"
        MQTTClient.logger.warn(msg)
        try:
            MQTTClient.logger.info(f"Attempting to reconnect to {self.broker_ip}:{self.port}")
            self.client.connect(self.broker_ip, self.port)
            MQTTClient.logger.info(f"Reconnected to {self.broker_ip}:{self.port}")
        except Exception as e:
            MQTTClient.logger.exception(e.message)
            raise ConnectionError(e.message)

    def _on_connect_fail(self):
        msg = f"Failed to connect to {self.broker_ip} @ port {self.port}"
        MQTTClient.logger.critical(msg)
        raise ConnectionRefusedError(msg)

    def _on_connect(self):
        MQTTClient.logger.info(f"Connected to {self.broker_ip} @ port {self.port}")

    def publish(self, topic, msg):
        MQTTClient.logger.debug(f"Attempting to publish {msg} to /{topic}")
        if topic in self.chosen_commands and msg.lower() in IOTClient.ALLOWED_COMMANDS.get(topic):
            mqttMessageInfo = self.client.publish(topic, msg)
            return mqttMessageInfo.is_published
        
        return False

    def subscribe(self, topic):
        if topic in self.chosen_commands:
            return self.client.subscribe(topic)
        else:
            return False

    def loop_forever(self):
        MQTTClient.logger.info(f"{self.__class__.__name__} on loop forever")
        self.client.loop_forever()
    
