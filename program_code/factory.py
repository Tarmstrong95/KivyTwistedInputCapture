from twisted.internet import protocol
from kivy.logger import Logger
import time, typing
from client import Client
from queue import Queue

class Factory(protocol.ClientFactory):
    def __init__(self) -> None:
        self.IV_event_to_send: Queue = Queue()
        self.IV_client: Client = None

    def clientConnectionFailed(self, connector, reason) -> None:
        # Logger.error("Connection: failed - goodbye!")
        time.sleep(0.1)
        connector.connect()

    def clientConnectionLost(self, connector, reason) -> None:
        Logger.error("Connection: lost - goodbye!")
        connector.connect()

    def buildProtocol(self, addr: typing.Tuple[str, int]) -> Client:
        client: Client = Client()
        client.IV_factory = self
        self.IV_client = client
        return client

    def setEvent(self, event: dict) -> None:
        if self.IV_client is not None and self.IV_client.connected:
            self.IV_event_to_send.put(event)
            return
        Logger.error("SEND EVENT: Not Connected")