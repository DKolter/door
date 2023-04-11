from _thread import start_new_thread
from display import Display
from door import Door
from website import Website
from rtc import Rtc
from state import State
from sensors import Sensors
from connection import Connection
import log

rtc = Rtc()

try:
    state = State()
    display = Display(state, rtc)
    door = Door(state)
    start_new_thread(door.execute, (display, rtc))
    sensors = Sensors()
    website = Website()
    connection = Connection()
    website.serve(connection, state, display, sensors, rtc)
except Exception as e:
    log.write_error(log.format_exc(e), rtc)
