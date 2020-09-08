
import inbox, appuifw

box = inbox.Inbox()
query = appuifw.query(u"Type in the query", "text")

hits = [sms_id for sms_id in box.sms_messages()\
           if box.content(sms_id).find(query) != -1]
