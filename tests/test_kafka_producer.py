import importlib
import sys


class DummyProducer:
    def __init__(self):
        self.sent = []
        self.flushed = False

    def send(self, topic, value):
        self.sent.append((topic, value))

    def flush(self):
        self.flushed = True


def test_publish_wishlist_update_sends_payload(monkeypatch):
    dummy = DummyProducer()

    monkeypatch.setattr("kafka.KafkaProducer", lambda *args, **kwargs: dummy)

    sys.modules.pop("src.kafka.producer", None)
    producer_module = importlib.import_module("src.kafka.producer")
    importlib.reload(producer_module)

    payload = [{"name": "Item", "price": "10"}]
    producer_module.publish_wishlist_update(payload)

    assert dummy.sent == [("wishlist_prices", payload)]
    assert dummy.flushed is True
