import urllib

import simplejson

import sys

import appuifw,e32

def trance():

	app_lock = e32.Ao_lock()

	def quit():

    		print "Exit Key Pressed"

    		app_lock.signal()
def translate():

    		slang=[u"engilsh",u"spanish",u"french",u"german"]

    		tlang=[u"english",u"hindi",u"spanish",u"french",u"german"]

    		g=appuifw.popup_menu(slang,u"Select source language")

    		h=appuifw.popup_menu(tlang,u"Select translation language") 

    		if g == 0:

			sl="en"

    		elif g==1:

			sl="es"

    		elif g==2:

			sl="fr"

    		elif g==3:

			sl="de"		

    

    		if h==0:

			tl="en"

    		elif h==1:

			tl="hi"

    		elif h==2:

              		tl="es"

    		elif h==3:

			tl="fr"

    		elif h==4:

			tl="de"

    

    		langpair='%s|%s'%(sl,tl)

    		text = appuifw.query(u"Type text to convert","text",u"group 10 rocks")

    		base_url='http://ajax.googleapis.com/ajax/services/language/translate?'

    		data = urllib.urlencode({'v':1.0,'ie': 'UTF8', 'q': text.encode('utf-8'),

                             'langpair':langpair})

    		url = base_url+data

    		search_results = urllib.urlopen(url)

    		json = simplejson.loads(search_results.read())

    		result = json['responseData']['translatedText']

    		appuifw.note(result,"info")

    		app_lock.wait()

    		print result

	translate()

