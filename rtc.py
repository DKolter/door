import ntptime
import time


class Rtc(object):
    def __init__(self):
        self.time_check = 0

    def update_time(self):
        if self.time_check == 0:
            try:
                ntptime.settime()
            except Exception:
                return
        self.time_check = (self.time_check + 1) % 30

    def is_summertime(self):
        current = time.localtime(time.time() + 3600)

        end_of_march = time.mktime((current[0], 3, 31, 0, 0, 0, 0, 0))
        end_of_march = time.localtime(end_of_march)
        march_last_sunday = 31 - (end_of_march[6] + 1) % 7
        march_last_sunday = time.mktime(
            (current[0], 3, march_last_sunday, 0, 0, 0, 0, 0)) + 7200

        end_of_october = time.mktime((current[0], 10, 31, 0, 0, 0, 0, 0))
        end_of_october = time.localtime(end_of_october)
        october_last_sunday = 31 - (end_of_october[6] + 1) % 7
        october_last_sunday = time.mktime(
            (current[0], 10, october_last_sunday, 0, 0, 0, 0, 0)) + 10800

        return march_last_sunday <= time.time() <= october_last_sunday

    def is_daylight(self):
        dst_offset = self.is_summertime() * 3600 + 3600
        localtime = time.localtime(time.time() + dst_offset)
        return 7 <= localtime[3] <= 18

    def time_to_str(self, when=None):
        if when == None:
            when = time.time()

        localtime = time.localtime(when + 3600 + self.is_summertime() * 3600)
        hour = f"{localtime[3]:02d}:{localtime[4]:02d}"
        today = time.mktime(
            (localtime[0], localtime[1], localtime[2], 0, 0, 0, 0, 0)) - 3600 - self.is_summertime() * 3600
        yesterday = today - 86400

        if when >= today:
            day = "today"
        elif when >= yesterday:
            day = "yesterday"
        else:
            day = f"{localtime[2]}.{localtime[1]}"

        return f"{hour} {day}"
