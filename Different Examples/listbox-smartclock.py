#
# SmartClock - The Intelligent Talking Clock
#
# Created by Taha M -- http://series-sixty.blogspot.com
#

import appuifw, audio, time, e32

def exit_key_handler():
 if appuifw.query(u'Exit now?','query') == True: 
  appuifw.note(u"For updates and more info, visit series-sixty.blogspot.com")
  app_lock.signal()
  appuifw.app.set_exit()

def hide_all():
 try: appuifw.e32.start_exe(u'z:\\sys\\bin\\phone.exe','')
 except: pass

def help():
 appuifw.note(u"SmartClock reads the current time out aloud whenever it is brought into the foreground")
 appuifw.note(u"You do not need to press any keys as this is automatic") 
 appuifw.note(u"It can also read the current time out aloud after a user-defined delay")
 appuifw.note(u"This can be useful whenever you wish to be notified of the time regularly without fail")
 appuifw.note(u"Note that: \n1 min = 60 secs \n30 min = 1,800 secs\n1 hr = 3,600 secs\n24 hrs = 86,400 secs") 
 appuifw.note(u"For updates and more info, visit series-sixty.blogspot.com")

def about():
 try: audio.say(u'Smart Clock, Version One point zero ')
 except: pass
 appuifw.note(u"SmartClock \nVersion 1.0\n\nCreated By Taha M \nThe Series 60 Weblog", "info")
 appuifw.note(u"For updates and more info, visit series-sixty.blogspot.com")

def call(focus):
 if focus == 1:
  clock()

num =[u"O, Clock",u"One",u"Two",u"Three",u"Four",u"Five",u"Six",u"Seven", 
u"Eight", 
u"Nine", 
u"Ten", 
u"Eleven",
u"Twelve", 
u"Thirteen",
u"Fourteen",
u"Fifteen",
u"Sixteen"
u"Seventeen",
u"Eighteen",
u"Nineteen",
u"Twenty", 
u"Twenty one",
u"Twenty two",
u"Twenty three",
u"Twenty four", 
u"Twenty five",
u"Twenty six",
u"Twenty seven",
u"Twenty eight",
u"Twenty nine",
u"Thirty",
u"Thirty one",
u"Thirty two",
u"Thirty three",
u"Thirty four", 
u"Thirty five",
u"Thirty six",
u"Thirty seven",
u"Thirty eight",
u"Thirty nine",
u"Forty",
u"Forty one",
u"Forty two",
u"Forty three",
u"Forty four",
u"Forty five",
u"Forty six",
u"Forty seven",
u"Forty eight",
u"Forty nine",
u"Fifty",
u"Fifty one",
u"Fifty two",
u"Fifty three",
u"Fifty four", 
u"Fifty five",
u"Fifty six",
u"Fifty seven",
u"Fifty eight",
u"Fifty nine",
u"Fifty nine"]

def parent1():
 global delay
 delay = appuifw.query(u'Enter delay (in seconds):','number')
 if delay < 10:
  appuifw.note(u"Please set the delay to a value greater than or equal to 10 secs")
  delay = appuifw.query(u'Enter delay (in seconds):','number')
  if delay < 10:
   appuifw.note(u"Automatically setting the delay to 5 mins")
   delay = 300
 if delay > 86400:
  appuifw.note(u"Please set the delay to a reasonable value")
  delay = appuifw.query(u'Enter delay (in seconds):','number')
  if delay > 86400:
   appuifw.note(u"Automatically setting the delay to 5 mins")
   delay = 300
 parent()

def parent():
 clock()
 e32.ao_sleep(delay, parent) 

def clock():
 h = time.strftime("%I",time.localtime())
 m = time.strftime("%M",time.localtime())
 if int(m) < 1:
  min = u" " + num[int(m)]
 elif int(m) < 2:
  min = u"O, " + num[int(m)]
 elif int(m) < 10:
  min = u"O, " + num[int(m)]
 elif int(m) > 59:
  min = u" " + num[int(m)]
 else:
  min= num[int(m)]
 s = time.strftime("%S",time.localtime())
 p = time.strftime("%p",time.localtime())
 if p == u"PM":
  p = u" Peeee M"
 else:
  p = u" Aaay M"
 current = num[int(h)]+ u","  + min + u" , "  + p
 try: audio.say(current)
 except: pass

def menu():
 def handler():
  index = lb.current()
  if index == 0:
   if s1 == u'1. Status : Active':
    menu()
  elif index == 1:
   if s2 == u'2. Set Delay':
    parent1()
    menu()
  elif index == 2:
   if s3 == u'3. About':
    about()
    menu()
  elif index == 3:
   if s4 == u'4. Help':
    help()
    menu()
 s1 = u'1. Status : Active'
 s2 = u'2. Set Delay'
 s3 = u'3. About'
 s4 = u'4. Help'
 entries = [s1,s2,s3,s4]
 lb = appuifw.Listbox(entries,handler)
 appuifw.app.body = lb
 appuifw.app.menu=[(u'Minimize all',hide_all),(u'Exit',exit_key_handler)]
 appuifw.app.title = u"SmartClock"
 appuifw.app.focus=call
 
appuifw.app.exit_key_handler = exit_key_handler
menu()
app_lock = e32.Ao_lock()
app_lock.wait()
