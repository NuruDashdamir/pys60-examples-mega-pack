# This script lets you write settings into a file on the OS and also lets you read them
# in this case I store 2 variables, each with a certain value.


# import os is needed to create a new directory or check whether a directory exists
import os


def write_settings():
    # write your settings:
    # define the directory where you want to store your settings
    CONFIG_DIR='e:/mynewfolder'
    # define the settings file
    CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')
    # make sure the settings file exists (created here when running the script for the first time).
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')
    # your settings:        
    value1 = 'man'
    value2 = 3.15
    # create an empty dictionary (to store your values attached to variables)
    config={}
    # attach value1 with variable1 and write them into the dictonary: {'variable1':'man'}
    config['variable1']= value1
    # attach value2 with variable2 and add them into the dictonary: {'variable1':'man' , 'variable2':'woman'}
    config['variable2']= value2
    # HINT: you can add here more variables and attach values to them freely as you wish. 
    # config['...']= ....
    # open the your "settings" file in "write mode" where to store the dictionary
    f=open(CONFIG_FILE,'wt')
    # write the dictinary into into the settings file
    f.write(repr(config))
    f.close()
    

def read_settings():
    # read your settings:
    # define the settings file where to read from
    CONFIG_FILE='e:/mynewfolder/mysettings.txt'
    try:
        # open the settings file in "read mode"
        f=open(CONFIG_FILE,'rt')
        try:
            # read the file
            content = f.read()
            # separate the content
            config=eval(content)
            f.close()
            # get the value that is attached to the variable
            value1=config.get('variable1','')
            value2=config.get('variable2','')
            print value1
            print value2
        except:
            print 'can not read file'
    except:
        print 'can not open file'

# call the write settings function    
write_settings()

# call the read settings function
read_settings()
