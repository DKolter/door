from errno import ETIMEDOUT, ECONNRESET
import log
import machine
from time import sleep


class Website(object):
    def __init__(self):
        with open("door.html", "r") as file:
            self.template = file.read()

    def hydrate(self, state, sensors, rtc, log_enabled):
        percentage, battery = sensors.read_battery()
        temperature = sensors.read_temperature()
        return self.template % (
            state.get_icon(),
            state.get_time(rtc),
            log.get_html() if log_enabled else "",
            percentage,
            battery,
            "./" if log_enabled else "./log",
            temperature
        )

    def serve(self, connection, state, display, sensors, rtc):
        while True:
            try:
                connection.check()
                rtc.update_time()
                display.screen_protection(rtc)
                request = connection.get_request()
                response = "done"

                if request in ["/", "/log"]:
                    response = self.hydrate(
                        state, sensors, rtc, request == "/log")

                elif request == "/state":
                    response = state.value

                elif request == "/restart":
                    while state.in_progress():
                        sleep(1)
                    machine.reset()

                elif request == '/opendoor' and state.is_closed():
                    state.set_opening()

                elif request == '/closedoor' and state.is_open():
                    state.set_closing()

                connection.send_response(response)

            except OSError as e:
                if e.errno in [ETIMEDOUT, ECONNRESET]:
                    continue
                log.write_error(log.format_exc(e), rtc)
            except IndexError:
                pass
            except Exception as e:
                log.write_error(log.format_exc(e), rtc)
