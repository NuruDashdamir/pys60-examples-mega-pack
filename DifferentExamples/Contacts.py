
import contacts, appuifw, telephone

name = appuifw.query(u'Call to', 'text')
db = contacts.open()
entries = db.find(name)
names = []
for item in entries:
        names.append(item.title)
if names:
    index = appuifw.selection_list(names, search_field=0)
    num = entries[index].find('mobile_number')
    if num:
        telephone.dial(num[0].value)
    else:
        appuifw.note(u'Missing mobile phone number', 'error')
else:
    appuifw.note(u'No matches','error')
