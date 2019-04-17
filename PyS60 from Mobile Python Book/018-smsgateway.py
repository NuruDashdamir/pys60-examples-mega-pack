
import messaging, inbox, e32

PHONE_NUMBER = "+189823801102"
nasty_words = ['Java', 'C++', 'Perl']

def message_received(msg_id):
     box = inbox.Inbox()
     msg = box.content(msg_id)
     sender = box.address(msg_id)
     box.delete(msg_id)
     for word in nasty_words:
          msg = msg.replace(word, "XXX")
     messaging.sms_send(PHONE_NUMBER, msg)
     print "Message from %s forwarded to %s" %\
            (sender, PHONE_NUMBER)

box = inbox.Inbox()
box.bind(message_received)

print "Gateway activated"
app_lock = e32.Ao_lock()
app_lock.wait()
