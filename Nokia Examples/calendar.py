# Copyright (c) 2008 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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