import os,e32,appuifw

def save_dict(list):
	global dict
	dict={}
	for index in list:
		dict[index[0]]=index[2]
	return True

def insert():
	global dict
	try:
		key, volume = appuifw.multi_query(u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430:', u'\u0421\u043e\u0434\u0435\u0440\u0436\u0438\u043c\u043e\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430:')
	except:
		pass
	else:
		dict[key]=volume
		form.insert(len(dict)-1, (key, 'text', volume))

def pop():
	global dict
	if len(dict)==1:
		appuifw.note(u'\u0424\u043e\u0440\u043c\u0430 \u0434\u043e\u043b\u0436\u043d\u0430 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0442\u044c \u0445\u043e\u0442\u044f \u0431\u044b \u043e\u0434\u0438\u043d \u044d\u043b\u0435\u043c\u0435\u043d\u0442.', 'error')
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
	key=appuifw.query(u'\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043c\u044f \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430.', 'text', u'\u0411\u0435\u0437\u044b\u043c\u044f\u043d\u043d\u044b\u0439')
	if key:
		if dict.has_key(key):
			appuifw.note(u'\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441 \u0442\u0430\u043a\u0438\u043c \u043a\u043b\u044e\u0447\u043e\u043c \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442.')
		else:
			appuifw.note(u'\u041d\u0435\u0442 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430 \u0441 \u0442\u0430\u043a\u0438\u043c \u043a\u043b\u044e\u0447\u043e\u043c.', 'error')

def get():
	global dict
	key=appuifw.query(u'\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043c\u044f \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430.', 'text', u'\u0411\u0435\u0437\u044b\u043c\u044f\u043d\u043d\u044b\u0439')
	if key:
		appuifw.note(dict.get(key, u'\u041d\u0435\u0442 \u0442\u0430\u043a\u043e\u0433\u043e \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430.'))

dict={u'\u0411\u0435\u0437\u044b\u043c\u044f\u043d\u043d\u044b\u0439': u'\u041f\u0443\u0441\u0442\u043e'}
form=appuifw.Form([(u'\u0411\u0435\u0437\u044b\u043c\u044f\u043d\u043d\u044b\u0439', 'text', u'\u041f\u0443\u0441\u0442\u043e')], appuifw.FFormAutoLabelEdit | appuifw.FFormDoubleSpaced)

form.save_hook=save_dict
form.menu=[
(u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c', insert),
(u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c', pop),
(u'\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c', clear),
(u'\u041a\u043b\u044e\u0447\u0438', keys),
(u'\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u044f', values),
(u'\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430', has_key),
(u'\u041d\u0430\u0439\u0442\u0438', get)]

if appuifw.app.full_name().lower().find(u"python")!=-1:
	appuifw.app.title=u'FormBox'
	os.abort=lambda:0

while 1:
	form.execute()
	if appuifw.query(u'\u0412\u044b\u0439\u0442\u0438 \u0438\u0437 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b?', 'query'):
		break

os.abort()