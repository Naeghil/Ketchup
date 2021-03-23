from ketchup_ui.parser import Parser
from ketchup_core.pomodoro import Pomodoro

from ketchup_core._orchestrator_functions import OrchestratorFunctions


# An orchestrator is a component (e.g. context)
# with the purpose (responsibility) of creating and storing
# other components and mediating the interaction among them
class KetchupOrchestrator(OrchestratorFunctions):
    def __init__(self):
        super(KetchupOrchestrator, self).__init__()
        self.alert_list = ["hey ketchup", "he catch up", "hey catch up", "he ketchup",
                           "hey petal", "haircut up", "hey get up", "he kept up"]



    # The following method runs the main loop of the app
    # Its name is important because it is related to the idea of
    # a Thread/Process object. If the orchestrator becomes
    # a subclass of these classes, the run method is usually central




    def no_command(self, command):
        if command != "":
            self.speaker.say("Sorry, I don't recognise the command " + command)
            self.speaker.say("Please, repeat")
        self.receptive = True

    def nothing(self, args):
        self.speaker.say("Ok")

    def start_pomodoro(self, args):
        if self.current_pomodoro:
            self.speaker.say("There is already a pomodoro running!")
        else:
            self.speaker.say("Sure, starting now!")
            self.current_pomodoro = Pomodoro(self.message_queue)
            self.current_pomodoro.start()
        self.give_update(args)

    def stop_pomodoro(self, args):
        if self.current_pomodoro:
            self.current_pomodoro.do_kill()
            self.speaker.say("Ok, I stopped it.")
            self.current_pomodoro = None
        else:
            self.speaker.say("You want to stop working without having even started?")
            self.speaker.say("There is no pomodoro running!")

    def pause_pomodoro(self, args):
        self.speaker.say("Ok, hope it's worth it!")
        self.current_pomodoro.pause()

    def resume_pomodoro(self, args):
        self.speaker.say("Welcome back then!")  # ??
        self.current_pomodoro.resume()
        self.give_update(args)

    def give_update(self, args):
        message = "You're doing a " + self.current_pomodoro.current_state() + " now, "
        message += "and have " + str(int(self.current_pomodoro.time_left().seconds/60)) + " minutes left. "
        p_left = self.current_pomodoro.pomodoro_left()
        p_total = self.current_pomodoro.pomodoro_total()
        stage = int(p_left*5/p_total)
        if stage > 3:  # This is doubtful as it doesn't work very good with <5 pomodoros
            adv = "still"
            motiv = ". We're only getting started!"
        elif stage < 3:
            adv = "only"
            motiv = ". We're almost done!"
        else:
            adv = ""
            motiv = ". We're halfway through!"
        message += "You " + adv + "have " + str(p_left) + " pomodoros left out of " + str(p_total) + motiv
        self.speaker.say(message)



    def notify(self):
        if self.message_queue.empty():
            return
        old, new, time_left = self.message_queue.get()
        if new == "done":
            self.speaker.say("You're done! Surely you've done amazing work!")
            self.current_pomodoro = None
            return
        if old == "pomodoro":
            self.speaker.say("The pomodoro is over! Enjoy your break!")
        else:
            self.speaker.say("Break is over! Come on, back to work!")
        self.speaker.say("You have " + str(int(time_left.seconds/60)) + " minutes left")

    def motivate(self, args):
        self.speaker.say(self.motivator.answer(args))

    def run(self):
        parser = Parser()
        self.speaker.say("Hi, I'm Ketchup. Say hey ketchup to attract my attention. Say help to have more information.")

        while self.is_running:
            inp = self.listener.listen()
            if self.receptive:
                self.receptive = False
                comm, arg = parser.parse(inp)
                try:
                    # noinspection PyArgumentList
                    self.commands[comm](arg)
                except KeyError:
                    self.no_command(comm)
            elif inp in self.alert_list:
                self.speaker.say("Yes?")
                self.receptive = True
            self.notify()

        if self.current_pomodoro:
            self.current_pomodoro.do_kill()
        self.listener.do_kill()
