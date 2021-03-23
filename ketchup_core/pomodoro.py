# This class should store a number of states related to the
# current pomodoro run, which should be examinable from the main process
# The class itself should be a Thread/Process in itself as it should not
# be blocked by user interaction, unless specified by said interaction

import time
import datetime as dt
from threading import Thread


class Pomodoro(Thread):
    def __init__(self, message_queue, p_dur=5, s_dur=5, l_dur=5, to_break=3, p_number=4, t_step=1):
        super(Pomodoro, self).__init__()
        self.message_queue = message_queue
        # Configuration
        pom_duration = dt.timedelta(0, p_dur)
        short_duration = dt.timedelta(0, s_dur)
        long_duration = dt.timedelta(0, l_dur)
        self.pomodoro_number = p_number  # Number of pomodoros
        self.step = dt.timedelta(0, t_step)  # Time before checking again

        # Counters
        self.schedule = [["pomodoro", pom_duration]]  # List of [state, duration_left]
        for i in range(1, self.pomodoro_number):
            if (i % to_break) == 0:
                self.schedule.append(["long break", long_duration])
            else:
                self.schedule.append(["short break", short_duration])
            self.schedule.append(["pomodoro", pom_duration])
        self.progress = 0
        # Flags
        self.running = True
        self.kill = False
        # Pomodoro Schedule

    # State check methods
    def current_state(self):
        try:
            return self.schedule[self.progress][0]
        except IndexError:
            return "done"

    def time_left(self):
        try:
            return self.schedule[self.progress][1]
        except IndexError:
            return dt.timedelta(0, 0)

    def pomodoro_total(self):
        return self.pomodoro_number

    def pomodoro_left(self):
        ctr = 0
        for it in self.schedule[:self.progress]:
            if it[0] == "pomodoro":
                ctr += 1
        return self.pomodoro_number - ctr

    # Time advancement methods
    def advance_step(self):
        time.sleep(self.step.seconds)
        if self.running:
            self.schedule[self.progress][1] -= self.step
            print(self.current_state() + ": " + str(self.time_left()) + " left", flush=True)
        else:
            print("On pause")
        if self.time_left().seconds == 0 or self.time_left().seconds > 3600:
            self.advance_progress()
        time.sleep(self.step.seconds)

    def advance_progress(self):
        old = self.current_state()
        self.progress += 1
        self.message_queue.put(("pomodoro", (old, self.current_state(), self.time_left())))

    # Management methods
    def pause(self):
        if self.running:
            self.running = False
            return True
        else:
            return False

    def resume(self):
        if self.running:
            return False
        else:
            self.running = True
            return True

    def do_kill(self):
        self.kill = True

    # When and how does it stop?
    def run(self):
        while self.current_state() != "done" and not self.kill:
            self.advance_step()
