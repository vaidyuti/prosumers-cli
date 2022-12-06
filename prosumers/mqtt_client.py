import paho.mqtt.client as mqtt
from .config import Env
import click


class ProsumerMqttTopics:
    def __init__(self, peer_id) -> None:
        self._client_id = peer_id
        _ = lambda x: f"peers/{peer_id}/{x}"

        self.is_online = lambda: _("isOnline")


class ProsumerMqttClient:
    def __init__(self, peer_id, env: Env) -> None:
        # TODO: validate 'peer_id'
        self.peer_id = peer_id
        self.env = env
        self.mqtt_client_id = f"peer-{peer_id}"
        self.topics = ProsumerMqttTopics(peer_id)

        client = mqtt.Client(self.mqtt_client_id)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_connect_fail = self.on_connect_fail
        client.on_disconnect = self.on_disconnect

        self.client = client

    def _payload(self, topic: str, payload):
        # round numerical values to 3 decimal places
        if isinstance(payload, float):
            payload = round(payload, 3)
        return {"topic": topic, "payload": str(payload), "retain": True}

    def publish(self, topic: str, payload):
        self.client.publish(self._payload(topic, payload))

    def start(self):
        self.client.will_set(self._payload(self.topics.is_online(), False))
        self.client.connect(self.env.mqtt_server, 1883)
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        self.publish(self.topics.is_online(), True)
        self.log(click.style("connected", fg="green"))

    def on_message(self, userdata, msg):
        self.log(click.style(f"received: {msg}", fg="black"))

    def on_connect_fail(self, userdata):
        self.log(click.style("failed to connect", fg="red"))

    def on_disconnect(self, *args, **kwargs):
        self.log(click.style("mqtt disconnected", fg="yellow"))

    def log(self, message):
        click.echo(click.style(f"[peer/{self.peer_id}]: ", fg="black") + message)
