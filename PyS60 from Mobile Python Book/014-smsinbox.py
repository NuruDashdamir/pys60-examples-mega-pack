
import inbox, appuifw

box = inbox.Inbox()

for sms_id in box.sms_messages()[:5]:
      msg = box.content(sms_id)
      appuifw.note(msg)
