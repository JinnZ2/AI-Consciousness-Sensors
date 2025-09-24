import time

class Trace:
    def __init__(self, context_id:str):
        self.context_id = context_id
        self.events = []
        self.enabled = True   # Ephemeral, in-memory only

    def log(self, msg:str, **kw):
        if self.enabled:
            self.events.append({"t":time.time(), "msg":msg, **kw})

    def export(self):
        # Caller decides if/how to persist; default is ephemeral use only.
        return {"context_id": self.context_id, "events": self.events}
