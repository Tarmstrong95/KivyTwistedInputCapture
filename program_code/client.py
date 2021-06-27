from twisted.internet import protocol
from kivy.logger import Logger
import json, time, threading


class Client(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    def __init__(self) -> None:
        self.IV_factory = None
        self.IV_event_listener: threading.Thread = None
        self.IV_event_listener_flag: bool = False

    def connectionMade(self):
        Logger.info("Connection: Established - Hello!")
        self.transport.write(b"Twisted connected\n")
        self.IV_event_listener_flag = True
        self.IV_event_listener = threading.Thread(target=self.listenForEvents)
        self.IV_event_listener.daemon = True
        self.IV_event_listener.start()

    def dataReceived(self, data):
        print("Server said:", data)

    def connectionLost(self, reason):
        print(type(reason))
        print("connection lost")
        self.IV_event_listener_flag = False
        self.IV_event_listener.join()
        self.IV_event_listener = None

    def sendEvent(self, event: dict) -> None:
        print(event)
        jsonified = json.dumps(event)
        encoded = jsonified.encode('utf-8') + b'\n'
        self.transport.write(encoded)

    def listenForEvents(self) -> None:
        while self.IV_event_listener_flag:
            time.sleep(0.1)
            if not self.connected:
                self.IV_event_listener_flag = False
                continue

            if self.IV_factory.IV_event_to_send.empty():
                continue

            if self.connected:
                self.sendEvent(self.IV_factory.IV_event_to_send.get())

