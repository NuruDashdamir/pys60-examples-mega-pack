import e32,os,sys,appuifw
from urllib import urlopen,quote
ru=lambda text:text.decode("utf-8")
mail=''
class error:
	flag=0
	def write(self,text):
		if self.flag:
			appuifw.app.body.add(ru(text))
                        appuifw.app.menu=[(ru("Отправить"),lambda:urlopen(quote(u'http://www.neten.org/send_mail.php?name=debugger&email='+mail+'&subject=bug_in_your_programm&message=The dear developer the mistake is found in your program'+text+'the request to arrange on its elimination. Yours faithfully arok debugger&submit=Send','/:=&?')))]
                        e32.Ao_lock().wait()
		else:
			appuifw.app.exit_key_handler=os.abort
			appuifw.app.body=appuifw.Text(ru("	В программе произошла ошибка. Пожалуйста отошлите данный текст разработчикам.\n"))
			appuifw.app.body.color=0xff0000
			self.flag=1
if appuifw.app.full_name().lower().find(u"python")==-1:
	sys.stderr=error()