import appuifw
planets = [ u'Mars', u'Earth', u'Venus' ]
prompt = u'Enter your home planet'
index = appuifw.popup_menu(planets, prompt)
appuifw.note(u'Hello ' + planets[index], u'info')
