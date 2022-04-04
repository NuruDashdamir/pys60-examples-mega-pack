import appuifw, e32, graphics, sys, os

def ru(text_ru): return text_ru.decode('utf-8') 

round=appuifw.Text()
round.color=0x000000
round.add(ru("\n\n\n\nCache Remover v1.00\n\n\n\n\n\n\n\n\n\nAuthor: 6120man."))
appuifw.app.body=round
appuifw.app.title=u'Cache Remover'
appuifw.app.screen='normal'
        
def quit():
 if appuifw.query(ru('Exit?'),'query')==1:
  appuifw.app.set_exit()
           
def opera():
    if os.path.exists("e:\\System\\data\\Opera\\cache4"):
        for name in os.listdir("e:\\System\\data\\Opera\\cache4"):
            full_name=os.path.join("e:\\System\\data\\Opera\\cache4", name)
            os.remove(full_name)
        os.rmdir("e:\\System\\data\\Opera\\cache4")
        if os.path.exists("c:\\System\\data\\Opera\\cache4"):
            for name in os.listdir("c:\\System\\data\\Opera\\cache4"):
                full_name=os.path.join("c:\\System\\data\\Opera\\cache4", name)
                os.remove(full_name)
            os.rmdir("c:\\System\\data\\Opera\\cache4")
        ok()
    else:
        ko()  
   
def operawidget ():
    if os.path.exists("e:\\System\\data\\Opera\\OpWidget\\cache"):
        for name in os.listdir("e:\\System\\data\\Opera\\OpWidget\\cache"):
            full_name=os.path.join("e:\\System\\data\\Opera\\OpWidget\\cache", name)
            os.remove(full_name)
        os.rmdir("e:\\System\\data\\Opera\\OpWidget\\cache")
        if os.path.exists("c:\\System\\data\\Opera\\OpWidget\\cache"):
            for name in os.listdir("c:\\System\\data\\Opera\\OpWidget\\cache"):
                full_name=os.path.join("c:\\System\\data\\Opera\\OpWidget\\cache", name)
                os.remove(full_name)
            os.rmdir("c:\\System\\data\\Opera\\OpWidget\\cache")
        ok()
    else:
        ko()


def ucweb ():
    if os.path.exists("e:\\Private\\2001F848\\WMLImageCache"):
        for name in os.listdir("e:\\Private\\2001F848\\WMLImageCache"):
            full_name=os.path.join("e:\\Private\\2001F848\\WMLImageCache", name)
            os.remove(full_name)
        os.rmdir("e:\\Private\\2001F848\\WMLImageCache")
        if os.path.exists("c:\\Private\\2001F848\\WMLImageCache"):
            for name in os.listdir("c:\\Private\\2001F848\\WMLImageCache"):
                full_name=os.path.join("c:\\Private\\2001F848\\WMLImageCache", name)
                os.remove(full_name)
            os.rmdir("c:\\Private\\2001F848\\WMLImageCache")
        ok()
    else:
        ko()


def ozone ():
    if os.path.exists("e:\\shared\\o3\\cache"):
        for name in os.listdir("e:\\shared\\o3\\cache"):
            full_name=os.path.join("e:\\shared\\o3\\cache", name)
            os.remove(full_name)
        os.rmdir("e:\\shared\\o3\\cache")
        if os.path.exists("c:\\shared\\o3\\cache"):
            for name in os.listdir("c:\\shared\\o3\\cache"):
                full_name=os.path.join("c:\\shared\\o3\\cache", name)
                os.remove(full_name)
            os.rmdir("c:\\shared\\o3\\cache")
        ok()
    else:
        ko()

def standart():
    if os.path.exists("c:\\cache"):
        for name in os.listdir("c:\\cache"):
            full_name=os.path.join("c:\\cache", name)
            os.remove(full_name)
        os.rmdir("c:\\cache")
        ok()
    else:
        ko()
		
def help_sym():
  appuifw.app.body.set(ru("Program <Cache Remover> is used for removing always hoarding cache (garbage, which stay in memory after downloading web-page). \n If you need to remove cache, select browser that you use. Program will delete cache automatically. \n If you often visit web-pages, use program to remove cache."))
  printout(ru("3)	Program <Cache Remover> is used for removing always hoarding cache (garbage, which stay in memory after downloading web-page). \n If you need to remove cache, select browser that you use. Program will delete cache automatically. \n If you often visit web-pages, use program to remove cache."))

def about_sym():
  appuifw.app.body.set(ru("Cache remover v1.00 \n \n Author: 6120man (Andrey Bobylev) \n See me in ICQ: 578418982. \n \n Great thank for Edyard  <Ic{E}man> Shumanski for translating program from Russian into English. \n ICQ: 575497079. \n \n Waiting for you comments and proposals! ;-)"))
  printout(ru("Cache remover v1.00 \n \n Author: 6120man (Andrey Bobylev) \n See me in ICQ: 578418982. \n \n Great thank for Edyard  <Ic{E}man> Shumanski for translating program from Russian into English. \n ICQ: 575497079. \n \n Waiting for you comments and proposals! ;-)"))
            
def ok():    
    appuifw.note(ru("Cache deleted"),"conf")

def ko():
    appuifw.note(ru("Cache not found"),"error")  

app_lock=e32.Ao_lock()
 
appuifw.app.menu=[(ru("Standard browser"),standart),(u"Opera 8.65",opera),(u"Opera Widgets Manager 9.50",operawidget),(u"UCWeb",ucweb),(u"Ozone Web Browser",ozone),(ru("-=======-"),list),(ru("About program..."),about_sym),(ru("Help"),help_sym),(ru("Exit"),quit)]

appuifw.app.exit_key_handler=quit
app_lock.wait()
