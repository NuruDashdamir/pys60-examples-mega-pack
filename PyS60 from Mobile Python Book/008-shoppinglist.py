
import appuifw
import messaging

foods = [u"cheese", u"sausage", u"milk", u"banana", u"bread"]

choices = appuifw.multi_selection_list(foods,'checkbox',1)

items_to_buy = []
for x in choices:
    items_to_buy.append(foods[x])

greetings = appuifw.query(u"Add some greetings?", "text", u"thanks!")
if greetings:
        items_to_buy.append(greetings)

shoppinglist = ", ".join(items_to_buy)
print "Sending SMS: " + shoppinglist
messaging.sms_send("+1234567", shoppinglist)

appuifw.note(u"Shoppinglist sent")
