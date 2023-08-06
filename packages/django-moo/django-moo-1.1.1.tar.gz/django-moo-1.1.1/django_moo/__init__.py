from threading import Thread
from .delay import delay_thread

t = Thread(target=delay_thread)
t.start()