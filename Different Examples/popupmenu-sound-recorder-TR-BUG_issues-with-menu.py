# -*- coding: 'utf-8' -*-
import os
from appuifw import *
import audio
running=1
def quit():
     global running
     running=0
     app.set_exit()
     app.exit_key_handler=quit
def record():
     try:
          soundname=query(u"Kayit ismi:", "text")
          global s
          quality=[u".wav", u".amr"]
          selectQUALITY=selection_list(quality)
          if selectQUALITY == 0:
            point=u".wav"
          if selectQUALITY == 1:
             point=u".amr"
          sound=u"e:\\sounds\\digital\\"+soundname+point
          s=audio.Sound.open(sound)
          s.record()
          note(u"Kaydediliyor!", "info")
     except:
               sound=u"e:\\sounds\\digital\\sound.amr"
               s=audio.Sound.open(sound)
               s.record()
               note(u"Kaydediliyor!", "info")
def stop():
     try:
         s.stop()
         s.close()
     except:
              note(u"once kayit et", "error")
def play():
     try:
         global dir, files, select
         fil=u"e:\\sounds\\digital\\"+files[select]
         global s
         s=audio.Sound.open(fil)
         s.play()
         note(u"Oynatiliyor!", "info")
     except:
              note(u"once kaydet!", "error")
while running:
       popupmenu=[u"Kayit", u"Durdur", u"Oynat", u"Cikis"]
       pop=popup_menu(popupmenu, u"Tr:mustafa038")
       if pop == 0:
          record()
       if pop == 1:
         stop()
       if pop == 2:
          play()
       if pop == 3:
         quit()
       dir="e:\\sounds\\digital"
       files=map(unicode, os.listdir(dir))
       select=selection_list(files)
       if select == 1:
          play()
app.exit_key_handler=app.set_exit()