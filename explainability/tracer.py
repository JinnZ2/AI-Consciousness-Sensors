class Trace:
    def __init__(self, session_id: str = ""):
        self.session_id = session_id
        self.events = []

    def log(self, event: str, **kwargs):
        self.events.append({"event": event, **kwargs})
