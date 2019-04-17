
import inbox, appuifw, e32

def show_list(msgs):
    msgs.sort()
    items = []
    for msg in msgs:
         items.append(msg[1][:15])
    appuifw.selection_list(items)

def sort_time():
    msgs = []
    for sms_id in box.sms_messages():
          msgs.append((-box.time(sms_id), box.content(sms_id)))
    show_list(msgs)

def sort_sender():
    msgs = []
    for sms_id in box.sms_messages():
          msgs.append((box.address(sms_id), box.content(sms_id)))
    show_list(msgs)

def sort_unread():
    msgs = []
    for sms_id in box.sms_messages():
          msgs.append((-box.unread(sms_id), box.content(sms_id)))
    show_list(msgs)

def quit():
    print "INBOX SORTER EXITS"
    app_lock.signal()

box = inbox.Inbox()
appuifw.app.exit_key_handler = quit
appuifw.app.title = u"Inbox Sorter"
appuifw.app.menu = [(u"Sort by time", sort_time),
                    (u"Sort by sender", sort_sender),
                    (u"Unread first", sort_unread)]

print "INBOX SORTER STARTED"
app_lock = e32.Ao_lock()
app_lock.wait()
