from .scenario import Scenario, Peer
from .config import Env
from .mqtt_client import ProsumerMqttClient
from utils.repeat import repeat


class TickablePeer:
    def __init__(self, peer: Peer, env: Env) -> None:
        self.peer = peer
        self.client = ProsumerMqttClient(peer.id, env)
        self.client.start()

    def tick(self):
        pass


class RunnableScenario:
    def __init__(self, scenario: Scenario, env: Env) -> None:
        self.scenario = scenario
        self.env = env
        self.peers = [TickablePeer(p, env) for p in scenario.peers]

    @repeat(interval=5)
    def run(self):
        for peer in self.peers:
            peer.run()
