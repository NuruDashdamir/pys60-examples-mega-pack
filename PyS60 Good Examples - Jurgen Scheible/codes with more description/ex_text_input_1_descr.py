# Copyright (c) 2005 Jurgen Scheible
# This script performs a query with a single-field dialog (text input field)
# and displays the users input as a pop-up note 


# 1. import the application user interface framework module
import appuifw

# 2. , 3. create a text input field:  appuifw.query(label, type) and variable
data = appuifw.query(u"Type a word:", "text")

# 4. create a pop-up note: appuifw.note(label, type)
appuifw.note(u"The typed word was: " + data, "info")



""" detailed description:

1. we import the "appuifw" module to handle UI widgets like text input fields and
   pop-up notes etc.
2. we create a single-field dialog (text input field) using the .query() function
   of the appuifw module.
   we include in the brackets 2 parameters:
   - label: as label we put the text u"Type a word:" (the u must be there because
            the phone understands only text declared as unicode, the high commas
            must be there because label must be given as a string)
   - type: as type we put "text". It declares the input field as text type
           (other possible types: "number", "date", "time", "query", "code")
   -> separate the the two parameters with a comma.
3. We create a variable called data, and by putting data = appui... we write
   the result of the text input field into this variable
   (after user has typed something when he/she runs the script)

4. We create a pop-up note using the .note() function of the appuifw module. 
    we include in the brackets the 2 parameters:
   - label: as label we put the text u"The typed word was: " + data 
            This is the text that will appear in the pop-up note. Again the text
            must be given as a string in highcommas.
            But our pop-up note shall also inculde the result that the user
            has typed in, therefore we add the content of our variable data to our label
            string by writing + data (adding the content of a variable to a string)            
   - type: as type we put "info". It declares the pop-up note as info. This puts
           an exclamationmark in the pop-up note (other possible types: "error","conf")
   -> again, separate the the two parameters with a comma.

"""