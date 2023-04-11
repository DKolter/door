import io
import sys

log = []


def write_error(error, rtc):
    print(error)
    time = rtc.time_to_str().split()[0]
    time_span = f"<span class=\"log-time\">[{time}]</span>"
    error_span = f"<span class=\"log-error\"> {error}</span>"
    log.insert(0, f"<p>{time_span}{error_span}</p>")
    if len(log) > 50:
        del log[-1]


def write_info(info, rtc):
    print(info)
    time = rtc.time_to_str().split()[0]
    time_span = f"<span class=\"log-time\">[{time}]</span>"
    info_span = f"<span class=\"log-info\"> {info}</span>"
    log.insert(0, f"<p>{time_span}{info_span}</p>")
    if len(log) > 50:
        del log[-1]


def format_exc(e):
    buf = io.StringIO()
    sys.print_exception(e, buf)
    return buf.getvalue()


def get_html():
    content = "\n".join(log)
    return f"<div class=\"log\">{content}</div>"
