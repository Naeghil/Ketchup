from ketchup_ui import Listener, Speaker
from ketchup_core import Motivator
from queue import Queue


class OrchestratorComponents:
    def __init__(self):
        # Message passing for asynchronicity
        self._msg_queue = Queue()
        # Components
        self.listener = Listener(self._msg_queue)
        self._speaker = Speaker()
        self.motivator = Motivator()
        self.current_pomodoro = None
        # Flags
        self.is_running = True

    def say(self, msg):
        if not isinstance(msg, list):
            msg = [msg]
        for m in msg:
            self._speaker.say(m)

    def get_operation(self):
        return self._msg_queue.get(block=True)

    def run_test(self):
        inp = ""
        print("Initiating test")
        self.listener.start()
        while inp != "exit":
            sender, inp = self.get_operation()
            print("Sender: "+sender)
            print("Message: "+inp)
        self.listener.do_kill()
