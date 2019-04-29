# Copyright (c) 2004 Nokia
# Programming example -- see license agreement for additional rights
# Simple GUI example 2

import socket
import urllib

import e32
import appuifw

choices =[(u"Los Angeles Intl Airport", "KLAX"),
          (u"Dallas/Fort Forth", "KDFW"),
          (u"New York/John F. Kennedy", "KJFK")]
choices_labels = [x[0] for x in choices]
        
weather_url_base = "http://weather.gov/data/current_obs/"
tempfile = "c:\\weather.xml"

def find_value(text, tag):
    "Find the value between <tag> and </tag> in text. Always returns a string"
    begin_tag = "<" + tag + ">"
    begin = text.find(begin_tag)
    end = text.find("</" + tag + ">")
    if begin == -1 or end == -1:
        return ""
    begin += len(begin_tag)
    return text[begin:end]

def handle_selection():
    index = lb.current()
    code = choices[index][1]
    weather_url = weather_url_base + code + ".xml"
    lb.set_list([u"Please wait..."])
    appuifw.note(u"Fetching "+ weather_url, 'info')
    try:
        urllib.urlretrieve(weather_url, tempfile)
        f = open(tempfile, 'r')
        weatherinfo = f.read()
        f.close()
        weather = find_value(weatherinfo, "weather")
        temperature_string = find_value(weatherinfo,
                                        "temperature_string")
        appuifw.popup_menu([(u"Weather", unicode(weather)), 
                            (u"Temperature", 
                             unicode(temperature_string))], 
                           unicode(code))
    except IOError:
        appuifw.note(u"Connection error to server", 'error')
    except:
        appuifw.note(u"Could not fetch information", 'error')
    lb.set_list(choices_labels)

def handle_add():
    pass

def handle_delete():
    pass

def exit_key_handler():
    app_lock.signal()

lb = appuifw.Listbox(choices_labels, handle_selection)

old_title = appuifw.app.title
appuifw.app.title = u"Weather report"
appuifw.app.body = lb
appuifw.app.menu = [(u"Add new item", handle_add),
                    (u"Delete item", handle_delete)]
appuifw.app.exit_key_handler = exit_key_handler

app_lock = e32.Ao_lock()
app_lock.wait()

appuifw.app.title = old_title

