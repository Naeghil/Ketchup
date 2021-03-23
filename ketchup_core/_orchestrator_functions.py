from ketchup_core._orchestrator_components import OrchestratorComponents
from ketchup_core.pomodoro import Pomodoro


class OrchestratorFunctions(OrchestratorComponents):
    def __init__(self):
        super(OrchestratorFunctions, self).__init__()
        self.receptive = False
        self.commands = {
            # Session functions
            "exit": self.stop_run,
            "help": self.give_help,
            "attend": self.make_receptive,
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
        msg = ["I am Ketchup, your pomodoro assistant, I'm here to make your days more productive!",
               "To tell me something, first attract my attention by saying hey ketchup. I won't listen otherwise.",
               "Once you have my attention, you can start a pomodoro session by telling me to start",
               "By default a session consists of four productive intervals, the pomodoros, each lasting 25 minutes.",
               "Between each interval, you will take a short break of 5 minutes.",
               "After each third pomodoro, you'll have a long 30 minutes break.",
               "You can pause or resume the session anytime. Also, you can ask for an update on what is going on.",
               "You can exit the application by saying exit"]
        self.say(msg)

    def make_receptive(self, args):
        self.receptive = True
        self.say("Yes?")

    # Command functions
    def no_command(self, command):
        self.say("Sorry, I don't understand " + command)
        self.say("Please, repeat")
        self.receptive = True

    def nothing(self, args):
        self.say("Ok")

    # Pomodoro functions
    def start_pomodoro(self, args):
        if self.current_pomodoro:
            self.say("There is already a pomodoro running!")
        else:
            self.say("Sure, starting now!")
            self.current_pomodoro = Pomodoro(self._msg_queue)
            self.current_pomodoro.start()
        self.give_update(args)

    def give_update(self, args):
        message = "You're doing a " + self.current_pomodoro.current_state() + " now, "
        message += "and have " + str(int(self.current_pomodoro.time_left().seconds/60)) + " minutes left. "
        p_left = self.current_pomodoro.pomodoro_left()
        p_total = self.current_pomodoro.pomodoro_total()
        stage = int(p_left*5/p_total)
        if stage > 3:
            adv = "still"
            motiv = ". We're only getting started!"
        elif stage < 3:
            adv = "only"
            motiv = ". We're almost done!"
        else:
            adv = ""
            motiv = ". We're halfway through!"
        message += "You " + adv + "have " + str(p_left) + " pomodoros left out of " + str(p_total) + motiv
        self.say(message)

    def pause_pomodoro(self, args):
        self.say("Ok, hope it's worth it!")
        self.current_pomodoro.pause()

    def resume_pomodoro(self, args):
        self.say("Welcome back then!")  # ??
        self.current_pomodoro.resume()
        self.give_update(args)

    def stop_pomodoro(self, args):
        if self.current_pomodoro:
            self.current_pomodoro.do_kill()
            self.say("Ok, I stopped it.")
            self.current_pomodoro = None
        else:
            self.say("You want to stop working without having even started?")
            self.say("There is no pomodoro running!")

    def notify(self, old, new, time_left):
        if new == "done":
            self.say("You're done! Surely you've done amazing work!")
            self.current_pomodoro = None
            return
        if old == "pomodoro":
            self.say("The pomodoro is over! Enjoy your break!")
        else:
            self.say("Break is over! Come on, back to work!")
        self.say("You have " + str(int(time_left.seconds/60)) + " minutes left")

    # Motivation functions
    def motivate(self, args):
        self.say(self.motivator.answer(args))

# TODO: ideally interaction phrase construction and selection should be given to an appropriate class
