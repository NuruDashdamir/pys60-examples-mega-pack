import os, appuifw

home_dir = u'e:\\python\\'
tx_chose = u'Script to run?'

appuifw.app.title = tx_chose
py_files = []
all_files = os.listdir(home_dir)

for file_n in all_files:
	if file_n.lower().endswith('.py'): py_files.append(u''+file_n)
chose = appuifw.selection_list(py_files,1)

if chose != None:
	execfile(home_dir+py_files[chose])

appuifw.app.set_exit()
