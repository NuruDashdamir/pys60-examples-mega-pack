
import inbox, appuifw

box = inbox.Inbox()
query = appuifw.query(u"Search for:", "text").lower()

hits = []
ids = []
for sms_id in box.sms_messages():
      msg = box.content(sms_id).lower()
      if msg.find(query) != -1:
           hits.append(msg[:25])
           ids.append(sms_id)

index = appuifw.selection_list(hits, 1)
if index >= 0:
        appuifw.note(box.content(ids[index]))
