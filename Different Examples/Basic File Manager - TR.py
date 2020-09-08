# -*- coding: utf-8 -*-
# s60 dosya tarayýcýsý denemesi
# coded by rohanrhu
 
import os
from appuifw import *
 
app.title = u"Dosya Tarayicisi"
 
while True:
    liste = [u"x Cikis", u"< Geri"]
    for i in os.listdir(os.getcwd()): liste.append(unicode(i))
 
    i = selection_list(liste, 1)
    if liste[i] == u"x Cikis": break;
    elif liste[i] == u"< Geri":
        os.chdir("/".join(os.getcwd()[:-2].split("/")[:-1]) + "//")
        continue;
    else: os.chdir("%s%s" % (os.getcwd(), liste[i]))