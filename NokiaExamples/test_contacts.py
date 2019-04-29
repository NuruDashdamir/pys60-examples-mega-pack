#
# test_contacts.py
#
# Copyright (c) 2005 Nokia. All rights reserved.
#

#
# PLEASE TRY THIS WITH A MOBILE DEDICATED TO TESTING PURPOSES ONLY.
#

import contacts
import time


# script 1, iterate through contact entries in the default database.

# open the default database.
def script1():
    db=contacts.open()
    for id in db:
        print 'Contact:%s'%db[id]
    print 'number of entries:%i'%len(db)


# script 2, create new empty database and contact.

def script2():
    # create new, empty database.
    db=contacts.open('test_database','n')
       
    # add new contact.
    contact=db.add_contact()
    contact.add_field('first_name',value='John',label='Nickname')
    contact.add_field('last_name','Doe')
    contact.add_field('date',time.time())
    contact.add_field('mobile_number','76476548','work')
    contact.add_field(type='mobile_number',value='8764573',location='home')
    contact.commit()

    # print contact's data.
    for entry_id in db:
        contact=db[entry_id]
        print '**********'
        print 'the contact:%s'%contact
        print 'entry\'s id:%s'%contact.id
        print 'last_modified:%s'%time.ctime(contact.last_modified)
        print 'number of fields:%s'%len(contact)
        print 'field data:'
        print '----------'
        for field in contact:
            print 'label:%s'%field.label
            if field.schema['storagetype']=='datetime':  
                print 'value:%s'%time.ctime(field.value)
            else:
                print 'value:%s'%field.value
            print 'type:%s'%field.type
            print 'location:%s'%field.location
            print '----------'


# script 3, modify and delete.

def script3():
    # open the database, create if does not exist.
    db=contacts.open('test_database','c')
    
    # add new contact.
    contact=db.add_contact()

    # delete all the default fields
    while len(contact):
        del contact[0]

    # add new fields
    contact.add_field('first_name',value='John',label='Nickname')
    contact.add_field('last_name','Doe')
    contact.commit()
    
    print 'the contact at first:%s'%contact
    
    # modify the first of 'first_name' fields.
    contact.find('first_name')[0].value='Henry'
    
    print 'the contact now:%s'%contact
    
    # delete the first of 'first_name' fields.
    del contact[contact.find('first_name')[0].index]
    
    print 'and now:%s'%contact
    
    # delete the contact.
    del db[contact.id]


#script 4, export (and print) some vcards.

def script4():
    # open and empty the database, create if does not exist.
    db=contacts.open('test_database','n')
    
    # add new contacts.
    contact1=db.add_contact()
    contact1.add_field('first_name',value='Bill',label='Nickname')
    contact1.add_field('last_name','Mason')
    contact1.commit()
    
    contact2=db.add_contact()
    contact2.add_field('first_name','Julie')
    contact2.add_field('last_name','Richards')
    contact2.add_field('mobile_number',value='76476547',location='work')
    contact2.add_field('mobile_number',value='76476548',location='home')
    contact2.commit()
        
    vcards=db.export_vcards((contact1.id,contact2.id))

    # print the vcard string (contains contact1 and contact2).
    print vcards

    # print contact1 as vcard.
    print contact1.as_vcard()
    

# script 5, export and import some vcards.

def script5():
    # open and empty the database, create if does not exist.
    db=contacts.open('test_database','n')
    
    # get available field types.
    fieldtypes=db.field_types()
    
    # add new contacts.
    contact1=db.add_contact()
    contact1.add_field('first_name',value='Bill',label='Nickname')
    contact1.add_field('last_name','Mason')
    contact1.commit()
    
    contact2=db.add_contact()
    contact2.add_field('first_name','Julie')
    contact2.add_field('last_name','Richards')
    contact2.add_field('mobile_number',value='76476547',location='work')
    contact2.add_field('mobile_number',value='76476548',location='home')
    contact2.commit()
    
    # export 'Bill' and 'Julie'.
    vcards=db.export_vcards((contact1.id,contact2.id))
    
    print '***see bill and julie here***'
    for entry_id in db:
        print 'the contact:%s'%db[entry_id]
    print ''
    
    # delete 'Bill'.
    del db[contact1.id]

    print '***now bill has been deleted***'
    for entry_id in db:
        print 'the contact:%s'%db[entry_id]
    print ''
    
    # import 'Bill' and 'Julie'.
    db.import_vcards(vcards)
    
    print '***now bill is imported back in vcard***'
    for entry_id in db:
        print 'the contact:%s'%db[entry_id]


# script 6, find functionality.

def script6():
    # open and empty the database, create if does not exist.
    db=contacts.open('test_database','n')

    # get available field types.
    fieldtypes=db.field_types()
    
    # add new contacts.
    contact1=db.add_contact()
    contact1.add_field('first_name',value='Bill',label='Nickname')
    contact1.add_field('last_name',value='Mason')
    contact1.add_field('country','United States')
    contact1.commit()
    
    contact2=db.add_contact()
    contact2.add_field('first_name','Julie')
    contact2.add_field('last_name','Richards')
    contact2.add_field('country','Canada')
    contact2.commit()

    # search by string.
    
    print 'search results for \'ichar\':'
    search_results=db.find('ichar')
    print search_results
    print ''
    
    print 'search results for \'i\':'
    search_results=db.find('i')
    print search_results
    print ''  


# script 7, autocommit functionality.

def script7():
    # open and empty the database, create if does not exist.
    db=contacts.open('test_database','n')

    # add a contact.
    contact=db.add_contact()

    # delete all the default fields
    while len(contact):
        del contact[0]
        
    contact.add_field('first_name',value='Bill',label='Nickname')
    contact.add_field('last_name',value='Mason')
    contact.commit()

    # get first of contact's 'first_name' fields.
    field=contact.find('first_name')[0] 
    field.value='Jack' # change the name.

    print db[contact.id] # autocommit is on (since the name has changed in the database).

    contact.begin()
    field.value='John'
    print db[contact.id] # autocommit is off (since the name has not changed in the database).
    contact.commit() # save the changes.

    print db[contact.id] # commit() saved the changes (since the name has changed in the database).

    field.value='Henry'
    print db[contact.id] # autocommit is on again (since the name is changed in the database).


# script 8, compacting.

def script8():
    # open the database.
    db=contacts.open()
    
    # compact if required.
    if(db.compact_required()):
        db.compact()
        print 'compacting done'
    else:
        print 'no need to compact'


# script 9, schema.

def script9():
    # open and empty the database, create if does not exist.
    db=contacts.open('test_database','n')

    # add a contact.
    contact=db.add_contact()
    contact.add_field('first_name',value='Bill',label='Nickname')
    contact.add_field('date',value=time.time())
    contact.commit()

    # print information about the field types.
    print contact.find('first_name')[0].schema
    print contact.find('date')[0].schema


# script 10, field types.

def script10():
    # open the default database.
    db=contacts.open()

    # print information about all field types this database supports.
    print db.field_types()

    
import appuifw
import e32
lock=e32.Ao_lock()
appuifw.app.menu=[
    (u'show default db',script1),
    (u'create db and contact',script2),
    (u'modify and delete',script3),
    (u'vcard export',script4),
    (u'vcard export&import',script5),
    (u'find',script6),
    (u'autocommit test',script7),
    (u'compact',script8),
    (u'schema',script9),
    (u'field types',script10),
    (u'Exit',lock.signal)]
old_exit_handler=appuifw.app.exit_key_handler
def exit_handler():
    appuifw.app.exit_key_handler=old_exit_handler
    lock.signal()

appuifw.app.exit_key_handler=exit_handler
lock.wait()



