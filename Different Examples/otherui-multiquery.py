# This script creates 2 text input fields on one screen
# It uses the multi_query function of the appuifw module

# import the application user interface framework module
import appuifw

# create 2 text input fields at the same time:  appuifw.multi_query(label1, label2)
data1,data2 = appuifw.multi_query(u"Type your first name:",u"Type your surname:")

# print the reuslts on the screen
print data1
print data2