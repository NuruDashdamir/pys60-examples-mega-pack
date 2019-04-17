import os

def write_settings():
    CONFIG_DIR='e:/mynewfolder'
    CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')
    value1 = 'man'
    value2 = 3.15
    config={}
    config['variable1']= value1
    config['variable2']= value2
    f=open(CONFIG_FILE,'wt')
    f.write(repr(config))
    f.close()

def read_settings():
    CONFIG_FILE='e:/mynewfolder/mysettings.txt'
    try:
        f=open(CONFIG_FILE,'rt')
        try:
            content = f.read()
            config=eval(content)
            f.close()
            value1=config.get('variable1','')
            value2=config.get('variable2','')
            print value1
            print value2
        except:
            print 'can not read file'
    except:
        print 'can not open file'

write_settings()
read_settings()
