import pyinotify
from datetime import datetime
wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "CREATED", event.pathname,str(datetime.now())

    def process_IN_DELETE(self, event):
        print "DELETED:", event.pathname,str(datetime.now())

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/home', mask, rec=True)

notifier.loop()
