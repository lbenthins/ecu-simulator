import obd_listener
import _thread

_thread.start_new_thread(obd_listener.start, ())

print("OBD Listener started")
