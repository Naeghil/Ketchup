from ketchup_ui.parser import Parser
from ketchup_core._orchestrator_functions import OrchestratorFunctions


class KetchupOrchestrator(OrchestratorFunctions):
    def __init__(self):
        super(KetchupOrchestrator, self).__init__()
        self.parser = Parser()

    def do_operation(self, sender, instruction):
        if sender == "listener":
            self.do_user_operation(instruction)
        elif sender == "pomodoro":
            self.notify(*instruction)
        else:
            raise ValueError("Unexpected sender from message queue")

    def do_user_operation(self, user_in):
        if user_in:
            comm, *args = self.parser.parse(user_in)
            if self.receptive:
                try:
                    self.receptive = False
                    # noinspection PyArgumentList
                    self.commands[comm](args)
                except KeyError:
                    self.no_command(comm)
            elif comm == "attend":
                self.make_receptive(args)

    def terminate(self):
        if self.current_pomodoro:
            self.current_pomodoro.do_kill()
        self.listener.do_kill()

    def run(self):
        self.listener.start()
        self.say("Hi, I'm Ketchup. Say hey ketchup to attract my attention. Then say help to have more information.")
        while self.is_running:
            print("Waiting for operation")
            self.do_operation(*self.get_operation())

        self.terminate()
