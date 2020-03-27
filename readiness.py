import threading, os, settings
from pathlib import Path
from time import sleep

WAIT_SECONDS = int(os.getenv("WAIT_SECONDS"))


def touch_file():
    while True:
        # print('touching')
        Path("/tmp/health").touch()
        sleep(WAIT_SECONDS)


timer = threading.Thread(target=touch_file, name="Thread-timer")
timer.daemon = True
timer.start()
