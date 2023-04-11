import time


class State(object):
    def __init__(self):
        self.time = None
        try:
            f = open("state.txt", "r")
            self.value = f.read()
            f.close()
        except OSError:
            self.value = "closed"

    def write(self):
        f = open("state.txt", "w")
        f.write(self.value)
        f.close()

    def set_closed(self):
        self.value = "closed"
        self.time = time.time()

    def set_closing(self):
        self.value = "closing"

    def set_opening(self):
        self.value = "opening"

    def set_open(self):
        self.value = "open"
        self.time = time.time()

    def is_closed(self):
        return self.value == "closed"

    def is_closing(self):
        return self.value == "closing"

    def is_open(self):
        return self.value == "open"

    def is_opening(self):
        return self.value == "opening"

    def in_progress(self):
        return self.value in ["opening", "closing"]

    def get_icon(self):
        return [
            "https://cdn-icons-png.flaticon.com/512/4634/4634114.png",
            "https://cdn-icons-png.flaticon.com/512/4634/4634120.png",
        ][self.is_open() or self.is_closing()]

    def get_time(self, rtc):
        if self.time == None:
            return ""
        return f"{self.value} since {rtc.time_to_str(self.time)}"
