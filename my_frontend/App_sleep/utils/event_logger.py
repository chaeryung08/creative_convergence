class EventLogger:
    def log(self, msg, data=None):
        print(f"[Event] {msg}", data or "")

event_logger = EventLogger()
