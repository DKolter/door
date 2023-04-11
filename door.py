from time import sleep
from machine import Pin, PWM
import log


class Door(object):
    def __init__(self, state):
        self.state = state
        self.open_pin = Pin(0, Pin.OUT)
        self.close_pin = Pin(15, Pin.OUT)
        self.pwm_pin = PWM(Pin(2))
        self.pwm_pin.freq(5000)
        self.pwm_pin.duty_u16(0)
        self.open_button = Pin(10, Pin.IN, Pin.PULL_DOWN)
        self.close_button = Pin(5, Pin.IN, Pin.PULL_DOWN)
        self.end_pin = Pin(22, Pin.IN, Pin.PULL_DOWN)

    def open(self, rtc):
        if self.end_pin.value():
            self.open_pin.value(1)
        duty = 0
        iterations = 0
        while self.end_pin.value():
            iterations += 1
            duty = min(duty + 6000, 65535)
            self.pwm_pin.duty_u16(duty)
            sleep(0.05)
            if iterations > 300:
                log.write_error("Limit switch not reached", rtc)
                break
        self.pwm_pin.duty_u16(0)
        self.open_pin.value(0)
        log.write_info("Opened", rtc)
        self.state.set_open()
        self.state.write()

    def close(self, rtc):
        self.close_pin.value(1)
        duty = 0
        for _ in range(10):
            duty = min(duty + 6000, 65535)
            self.pwm_pin.duty_u16(duty)
            sleep(0.05)
        self.pwm_pin.duty_u16(65535)
        sleep(4.5)
        self.pwm_pin.duty_u16(0)
        self.close_pin.value(0)
        log.write_info("Closed", rtc)
        self.state.set_closed()
        self.state.write()

    def poll_buttons(self):
        if self.open_button.value() and self.state.is_closed():
            self.state.set_opening()
        if self.close_button.value() and self.state.is_open():
            self.state.set_closing()

    def execute(self, display, rtc):
        while True:
            try:
                self.poll_buttons()
                if self.state.is_opening():
                    display.update(self.state)
                    self.open(rtc)
                    display.update(self.state)
                elif self.state.is_closing():
                    display.update(self.state)
                    self.close(rtc)
                    display.update(self.state)
                sleep(0.1)
            except Exception as e:
                log.write_error(log.format_exc(e), rtc)
