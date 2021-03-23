from ketchup_core._orchestrator_components import OrchestratorComponents


class OrchestratorFunctions(OrchestratorComponents):
    def __init__(self):
        super(OrchestratorFunctions, self).__init__()
        self.commands = {
            # Test function
            "repeat": self.say,
            # Session functions
            "exit": self.stop_run,
            "help": self.give_help,
            # Command functions
            "nothing": self.nothing,
            # Pomodoro functions
            "start": self.start_pomodoro,
            "pause": self.pause_pomodoro,
            "resume": self.resume_pomodoro,
            "stop": self.stop_pomodoro,
            "update": self.give_update,
            # Motivation functions
            "motivate": self.motivate
        }

    # Session functions
    def stop_run(self, args):
        self.is_running = False

    def give_help(self, args):
        msg = "I am Ketchup, your pomodoro assistant, I'm here to make your days more productive!"
        msg += "To tell me something, first attract my attention by saying hey ketchup. I won't listen otherwise."
        msg += "Once you have my attention, you can start a pomodoro session by telling me to start"
        msg += "By default a session consists of four productive intervals, the pomodoros, each lasting 25 minutes." \
               "Between each interval, you will take a short break of 5 minutes."\
               "After each third pomodoro, you'll have a long 30 minutes break."
        msg += "You can pause or resume the session anytime. Also, you can ask for an update on what is going on."
        msg += "You can exit the application by saying exit"

        self.speaker.say(msg)

