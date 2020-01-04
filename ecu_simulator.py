import obd_listener
from threading import Thread


Thread(target=obd_listener.start).start()
