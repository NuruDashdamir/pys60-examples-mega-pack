#appuifw overview

import appuifw
import e32

# u designates unicode string in python
itemListing = [u'aaaa',u'bbbb',u'cccc',u'dddd',u'eeee']


# singleQuery
def singleQuery():
	appuifw.app.body = None
	valore = appuifw.query(u'insert text', 'text' )
	valore = appuifw.query(u'insert code', 'code' )
	valore = appuifw.query(u'insert number', 'number' )
	valore = appuifw.query(u'insert date', 'date' )
	valore = appuifw.query(u'insert time', 'time' )
	valore = appuifw.query(u'query', 'query' )

# multiQuery    
def multiQuery():
	appuifw.app.body = None
	valore = appuifw.multi_query(u'insert text 1', u'insert text 2' )

# note    
def noteError():
	appuifw.app.body = None
	valore = appuifw.note(u'This is an error', 'error' )

def noteInformation():
	appuifw.app.body = None
	valore = appuifw.note(u'This is an Information', 'info' )

def noteConfirm():
	appuifw.app.body = None
	valore = appuifw.note(u'This is an Confirm', 'conf' )    

# popupMenu
def popupMenu():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	valore = appuifw.popup_menu( myList, u'My List' )

# selectionList	
def selectionListNoSearch():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	valore = appuifw.selection_list( myList, search_field=0 )

def selectionListWithSearch():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	valore = appuifw.selection_list( myList, search_field=1 )	# possible bug: the searchfield is not displayed


# multiSelectionList	
def multiSelectionListWithCheckboxNoSearch():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	valore = appuifw.multi_selection_list(myList , style='checkbox', search_field=0)

def multiSelectionListWithCheckboxWithSearch():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	valore = appuifw.multi_selection_list(myList , style='checkbox', search_field=1)	
	
def multiSelectionListWithCheckmarkNoSearch():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	valore = appuifw.multi_selection_list(myList , style='checkmark', search_field=0)

def multiSelectionListWithCheckmarkWithSearch():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	valore = appuifw.multi_selection_list(myList , style='checkmark', search_field=1)

# Form
def createFormEditModeOnly():
	appuifw.app.body = None
	flags = appuifw.FFormEditModeOnly
	f = appuifw.Form(getForm(), flags)
	f.execute()

	
def createFormViewModeOnly():
	appuifw.app.body = None
	flags = appuifw.FFormViewModeOnly
	f = appuifw.Form(getForm(), flags)
	f.execute()
	
def createFormAutoLabelEdit():
	appuifw.app.body = None
	flags = appuifw.FFormAutoLabelEdit
	f = appuifw.Form(getForm(), flags)
	f.execute()
	
def createFormAutoFormEdit():
	appuifw.app.body = None
	flags = appuifw.FFormAutoFormEdit
	f = appuifw.Form(getForm(), flags)
	f.execute()
	
def createFormDoubleSpaced():
	appuifw.app.body = None
	flags = appuifw.FFormDoubleSpaced
	f = appuifw.Form(getForm(), flags)
	f.execute()	
	
def getForm():
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	result  = []
	result.append((u"Text", 'text', u''))
	result.append((u"Number", 'number', int(0)))
	result.append((u"Date", 'date', float(0)))
	result.append((u"Time", 'time', float(0)))
	result.append((u"Combo", 'combo', ( myList, 0 )))
	return result
	
# Text
def createText():
	appuifw.app.body = None
	text = appuifw.Text()
	text.style = (appuifw.STYLE_BOLD|appuifw.STYLE_ITALIC|appuifw.STYLE_UNDERLINE)
	text.font = "annotation"
	text.color = (255,0,0)
	text.add(u'My text...\n')
	text.font = "title"
	text.color = (255,255,0)
	text.add(u'My text...\n')
	text.font = "legend"
	text.color = (0,0,0)
	text.add(u'My text...\n')	
	text.font = "dense"
	text.color = (0,0,255)
	text.add(u'My text...\n')	
	text.font = "normal"
	text.color = (0,255,255)
	text.add(u'My text...\n')	
	
	appuifw.app.body = text

# List
def createListSingleLine():
	appuifw.app.body = None
	myList = [u'apple', u'banana', u'cherry' ,u'orange', u'pear', u'strawberry']
	listbox = appuifw.Listbox(myList, lbox_observe)	
	appuifw.app.body = listbox
	
def createListDoubleLine():
	appuifw.app.body = None
	myList = [(u'apple',u'fruit 1'), (u'banana',u'fruit 2'), (u'cherry',u'fruit 3') ,(u'orange',u'fruit 4'), (u'pear',u'fruit 5'), (u'strawberry',u'fruit 6')]
	listbox = appuifw.Listbox(myList, lbox_observe)	
	appuifw.app.body = listbox	
	
	
def createListSingleLineWithIcon():
	appuifw.app.body = None
	icon1 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 28, 29) 
	icon2 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm ", 40, 41)	
	myList = [(u'Signal', icon1), (u'Battery', icon2)]
	listbox = appuifw.Listbox(myList, lbox_observe)	
	appuifw.app.body = listbox
	
def createListDoubleLineWithIcon():
	appuifw.app.body = None
	icon1 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 28, 29) 
	icon2 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm ", 40, 41)	
	myList = [(u'Sygnal',u'2/7', icon1), (u'Battery',u'5/7', icon2)]
	listbox = appuifw.Listbox(myList, lbox_observe)	
	appuifw.app.body = listbox		


def lbox_observe():
    indice = 0
    
def about():
    appuifw.app.body = None
    valore = appuifw.note(u'python course', 'info' )


def exit_handler():
    appuifw.app.exit_key_handler=old_exit_handler
    appuifw.app.title = old_title
    lock.signal()

# running inside RunL()
lock=e32.Ao_lock() 
appuifw.app.menu = [
	(u'Form Menu',
		( (u'Edit Mode Only',createFormEditModeOnly), (u'View Mode Only',createFormViewModeOnly), (u'Auto Label Edit',createFormAutoLabelEdit), (u'Auto Form Edit',createFormAutoFormEdit), (u'Double Spaced',createFormDoubleSpaced) ) ),
	(u'Text',createText),
	(u'List Menu',
		( (u'Single Line',createListSingleLine), (u'Double Line',createListDoubleLine), (u'Single Line With Icon',createListSingleLineWithIcon), (u'Double Line With Icon',createListDoubleLineWithIcon) ) ),
	(u'Single Query', singleQuery),
	(u'Multi Query',multiQuery),
	(u'Note',
		( (u'Error',noteError), (u'Information',noteInformation), (u'Confirm',noteConfirm) ) ), 
	(u'Popup Menu',popupMenu), 
	(u'SelectionList',
		( (u'No Search',selectionListNoSearch), (u'With Search',selectionListWithSearch) ) ),
	(u'Multi Selection List',
		( (u'Checkbox No Search',multiSelectionListWithCheckboxNoSearch), (u'Checkbox With Search',multiSelectionListWithCheckboxWithSearch), (u'Checkmark No Search',multiSelectionListWithCheckmarkNoSearch), (u'Checkmark With Search',multiSelectionListWithCheckmarkWithSearch) ) ),
	(u'About...',about)		
	]
appuifw.app.body = None
old_title = appuifw.app.title
appuifw.app.title = u"appuifw Demo"
old_exit_handler=appuifw.app.exit_key_handler
appuifw.app.exit_key_handler=exit_handler

lock.wait() # block here until signaled