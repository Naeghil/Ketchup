import speech_recognition as sr
from threading import Thread


class Listener(Thread):
    def __init__(self, queue):
        super(Listener, self).__init__()
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()
        self.message_queue = queue
        self.running = True

    def prep(self):
        self.rec.adjust_for_ambient_noise(self.mic)

    def listen(self) -> str:
        with self.mic as mic:
            self.prep()
            try:
                audio = self.rec.listen(mic, phrase_time_limit=2)
                # Possibility to run "show_all=True" for possible alternatives
                t_audio = self.rec.recognize_google(audio, language='en')
                print(t_audio)
            except sr.UnknownValueError as ex:
                t_audio = ""  # This is noise
            except sr.RequestError:
                # Internet is down or it failed. What to do?
                pass

            return t_audio

    def do_kill(self):
        self.running = False

    def run(self):
        print("Listener starting")
        while self.running:
            usr_in = ""
            while usr_in == "":
                usr_in = self.listen()
            print("Heard: "+usr_in)
            self.message_queue.put(("listener", usr_in))
