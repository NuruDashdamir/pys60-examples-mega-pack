import os, e32, appuifw

def save_dict(list):
	global dict
	dict={}
	for index in list:
		dict[index[0]]=index[2]
	return True

def insert():
	global dict
	try:
		key, volume = appuifw.multi_query(u'Item name:', u'Item content:')
	except:
		pass
	else:
		dict[key]=volume
		form.insert(len(dict)-1, (key, 'text', volume))

def pop():
	global dict
	if len(dict)==1:
		appuifw.note(u'The form must contain at least one item', 'error')
		return False
	else:
		element=form.pop()
		del dict[element[0]]
		return True

def clear():
	while pop():
		pass

def keys():
	global dict
	appuifw.query(u', '.join(dict.keys()), 'query')

def values():
	global dict
	appuifw.query(u', '.join(dict.values()), 'query')

def has_key():
	global dict
	key=appuifw.query(u'Enter item name.', 'text', u'Untitled')
	if key:
		if dict.has_key(key):
			appuifw.note(u'Item with this key exists')
		else:
			appuifw.note(u'There is no item with this key', 'error')

def get():
	global dict
	key=appuifw.query(u'Enter item name', 'text', u'Untitled')
	if key:
		appuifw.note(dict.get(key, u'No such element'))

dict={u'Untitled': u'Empty'}
form=appuifw.Form([(u'Untitled', 'text', u'Empty')], appuifw.FFormAutoLabelEdit | appuifw.FFormDoubleSpaced)

form.save_hook=save_dict
form.menu=[
(u'Add', insert),
(u'Delete', pop),
(u'Clear', clear),
(u'Keys', keys),
(u'Values', values),
(u'Check', has_key),
(u'Find', get)] 

if appuifw.app.full_name().lower().find(u"python")!=-1:
	appuifw.app.title=u'FormBox'
	os.abort=lambda:0

while 1:
	form.execute()
	if appuifw.query(u'Exit?', 'query'):
		break

os.abort()