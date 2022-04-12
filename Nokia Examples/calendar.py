import time, calendar

now = time.time()
cal = calendar.open()


# add new appointment
a = cal.add_appointment()
a.content = 'urgent meeting'
a.description = 'this is the description'
a.set_time(now+3600, now+7200) # start and end time
a.commit()
print 'Calendar added'
print '---------------------------------'
todaytime = time.mktime((2008,7,14,0,0,0,0,0,0))
daily_instances = cal.daily_instances(todaytime)
print "daily instances:" + str(daily_instances)

for entry_id in cal:
    ent=cal[entry_id]

    print 'id:%i'%ent.id
    for entry in daily_instances:
        if entry["id"] == ent.id:
            print 'content:%s'%ent.content
            print 'description:%s'%ent.description
            print 'originating:%d'%ent.originating
            print 'location:%s'%ent.location
            print 'start_time:%s'%time.ctime(ent.start_time)
            print 'end_time:%s'%time.ctime(ent.end_time)   
            print 'repeat:' 
    print ent.get_repeat()       
    print '--------'