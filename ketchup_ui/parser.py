class Parser:
    def __init__(self):
        self.alert_list = ["hey ketchup", "he catch up", "hey catch up", "he ketchup",
                           "hey petal", "haircut up", "hey get up", "he kept up"]

    # Format TBD
    def parse(self, inp: str):
        if inp in self.alert_list:
            return "attend", ""
        inp = inp.split()
        if len(inp) == 1:
            return inp[0], ""
        else:
            return inp[0], inp[1:]
