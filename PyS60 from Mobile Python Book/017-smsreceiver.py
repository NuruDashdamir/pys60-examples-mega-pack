
import inbox, appuifw, e32

def message_received(msg_id):
        box = inbox.Inbox()
        appuifw.note(u"New message: %s" % box.content(msg_id))
        app_lock.signal()

box = inbox.Inbox()
box.bind(message_received)

print "Waiting for new SMS messages.."
app_lock = e32.Ao_lock()
app_lock.wait()
print "Message handled!"
