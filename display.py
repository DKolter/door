from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB
import log


class Display(object):
    def __init__(self, state, rtc):
        try:
            i2c = I2C(1, sda=Pin(6), scl=Pin(7))
            self.display = SSD1306_I2C(128, 64, i2c)
            self.open_img = self.load_img("lockopen.pbm")
            self.opening_img = self.load_img("lockopening.pbm")
            self.closed_img = self.load_img("lockclosed.pbm")
            self.closing_img = self.load_img("lockclosing.pbm")
            self.invert_color = True
            self.time_check = 0
            self.update(state)
        except Exception as e:
            log.write_error(log.format_exc(e), rtc)
            self.display = None

    def load_img(self, path):
        with open(path, 'rb') as f:
            f.readline()  # Magic number
            f.readline()  # Creator comment
            f.readline()  # Dimensions
            data = bytearray(f.read())
        return FrameBuffer(data, 128, 64, MONO_HLSB)

    def screen_protection(self, rtc):
        if self.display == None:
            return

        try:
            if self.time_check == 0:
                self.invert_color = not rtc.is_daylight()
                self.display.invert(self.invert_color)
                self.display.show()
            self.time_check = (self.time_check + 1) % 30
        except Exception as e:
            log.write_error(log.format_exc(e), rtc)

    def update(self, state):
        if self.display == None:
            return

        self.display.blit({
            "closed": self.closed_img,
            "closing": self.closing_img,
            "open": self.open_img,
            "opening": self.opening_img,
        }[state.value], 0, 0)
        self.display.invert(self.invert_color)
        self.display.show()
