import appuifw,os,e32,string
def ru(x):
 return x.decode("utf-8")
def ur(x):
 return x.encode("utf-8")
def scan(path):
  if path=='':
    return e32.drive_list()
  if os.path.isdir(path)==0 and os.path.isfile(path)==0:
    return [u'<<<']
  _files=[]
  files=[u"<<<"]
  for _file in os.listdir(path):
    if os.path.isfile(path+_file)==0:
      _file+="\\"
      files.append(ru(_file))
    else:
      _files.append(ru(_file))
  files.extend(_files)
  return files
def fopen():
  app_lock.signal()
def info():
  return appuifw.app.body.current()
def back(path):
  if len(path)==3:return ''
  path=path.split('\\')[:-2]
  path= string.join(path,'\\')
  return path+'\\'
def exit():
 global run
 run=0
 app_lock.signal()
path=u''
run=1
app_lock = e32.Ao_lock()
lock=0
appuifw.app.exit_key_handler=exit
while run:
 files=scan(ur(path))
 if lock==0:
   appuifw.app.body=appuifw.Listbox(files,fopen)
 app_lock.wait()
 index=info()
 if len(path) == 0 :
    path=e32.drive_list()[index]+'\\'
    lock=0
 elif index==0 :
    path=back(ur(path))
    lock=0
 elif os.path.isfile(ur(path+files[index])):
    lock=1
 else:
    path+=files[index]
    lock=0