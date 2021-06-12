# Database example application: a sports diary.

# Copyright (c) 2005 Nokia Corporation
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


import time

import e32
import e32db
import appuifw

class SportsDiary:
    def __init__(self, db_name):
        try:
            self.native_db = e32db.Dbms()
            self.native_db.open(db_name)
        except:
            self.native_db.create(db_name)
            self.native_db.open(db_name)
            self.native_db.execute(SportsDiaryEntry.sql_create)
    
    def get_all_entries(self):
        dbv = e32db.Db_view()
        dbv.prepare(self.native_db,
                    u"SELECT * from events ORDER BY date DESC")
        dbv.first_line()
        results = []
        for i in range(dbv.count_line()):
            dbv.get_line()
            e = SportsDiaryEntry(dbv)
            results.append(e)
            dbv.next_line()
        return results
    
    def add(self, e):
        self.native_db.execute(e.sql_add())

    def delete(self, e):
        self.native_db.execute(e.sql_delete())

    def close(self):
        self.native_db.close()

class SportsDiaryEntry:
    sports = [u"Running", u"Skating", u"Biking", u"Skiing", u"Swimming"]
    sql_create = u"CREATE TABLE events (date TIMESTAMP, duration FLOAT, distance FLOAT, sport INTEGER, comment VARCHAR)"
    
    # Initialize with a row from Sport_diary_db
    def __init__(self, r=None):
        if r:            
            self.timestamp  = r.col(1)
            self.duration   = r.col(2)
            self.distance   = r.col(3)
            self.sport      = r.col(4)
            self.comment    = r.col(5)
        else:
            self.timestamp  = time.time()
            self.duration   = 0.0
            self.distance   = 0.0
            self.sport      = None
            self.comment    = u""

    def sql_add(self):
        sql = "INSERT INTO events (date, duration, distance, sport, comment) VALUES (#%s#,%d,%d,%d,'%s')"%(
            e32db.format_time(self.timestamp),
            self.duration,
            self.distance,
            self.sport,
            self.comment)
        return unicode(sql)
    
    def sql_delete(self):
        sql = "DELETE FROM events WHERE date=#%s#"%\
              e32db.format_time(self.timestamp)
        return unicode(sql)
    
    def unixtime(self):
        return self.timestamp
    
    def get_sport_text(self):
        return self.sports[self.sport]

    def get_form(self):
        # Convert Unix timestamp into the form the form accepts.
        (yr, mo, da, h, m, s, wd, jd, ds) = \
             time.localtime(self.timestamp)
        m += 60*h # 60 minutes per hour
        s += 60*m # 60 seconds per minute
        result = [(u"Date", 'date', float(self.timestamp-s)),
                  (u"Time", 'time', float(s)),
                  (u"Duration", 'time', float(self.duration)),
                  (u"Distance", 'number', int(self.distance))]
        if self.sport == None:
            result.append((u"Sport", 'combo', (self.sports, 0)))
        else:
            result.append((u"Sport", 'combo', (self.sports, self.sport)))
        result.append((u"Comment", 'text', self.comment))
        return result
    
    def set_from_form(self, form):
        self.timestamp = form[0][2]+form[1][2]
        self.duration  = form[2][2]
        self.distance  = form[3][2]
        self.sport     = form[4][2][1]
        self.comment   = form[5][2]
        

class SportsDiaryApp:
    def __init__(self):
        self.lock = e32.Ao_lock()
        self.exit_flag = False
        appuifw.app.exit_key_handler = self.abort
        self.main_view = appuifw.Listbox([(u"Loading...", u"")], 
                                         self.handle_view_entry)
        appuifw.app.body = self.main_view
        self.entry_list = []
        self.menu_add = (u"Add", self.handle_add)
        self.menu_summary = (u"Summary", self.handle_summary)
        self.menu_delete = (u"Delete", self.handle_delete)
        appuifw.app.menu = []

    def initialize_db(self, db_name):
        self.sports_diary = SportsDiary(db_name)
        
    def run(self):
        while not self.exit_flag:
            self.show_main_view()
            self.lock.wait()
        self.close()

    def close(self):
        appuifw.app.menu = []
        appuifw.app.body = None
        appuifw.app.exit_key_handler = None
        self.sports_diary.close()

    def abort(self):
        self.exit_flag = True
        self.lock.signal()

    def update_entry_list(self):
        self.entry_list = self.sports_diary.get_all_entries()
    
    def show_main_view(self):
        self.update_entry_list()
        if not self.entry_list:
            content = [(u"(Empty)", u"")]
        else:
            content = [(unicode(time.ctime(item.unixtime())), 
                        item.get_sport_text()) for item in self.entry_list]

        self.main_view.set_list(content)

        if not self.entry_list:
            appuifw.app.menu = [self.menu_add]
        else:
            appuifw.app.menu = [self.menu_add,
                                self.menu_delete,
                                self.menu_summary]

    def handle_add(self):
        new_entry = SportsDiaryEntry()
        data = new_entry.get_form()
        flags = appuifw.FFormEditModeOnly
        f = appuifw.Form(data, flags)
        f.execute()
        new_entry.set_from_form(f)
        self.sports_diary.add(new_entry)
        self.lock.signal()

    def handle_delete(self):
        if self.entry_list:
            index = self.main_view.current()
        if appuifw.query(u"Delete entry?", 'query'):
            self.sports_diary.delete(self.entry_list[index])
        self.lock.signal()

    def handle_summary(self):
        sum = 0
        for e in self.entry_list:
            sum += e.distance
        appuifw.note(u"Total distance is "+str(sum), 'info')
            
    def handle_view_entry(self):
        if self.entry_list:
            index = self.main_view.current()
            self.show_entry(self.entry_list[index])
        self.lock.signal()

    def show_entry(self, entry):
        data = entry.get_form()
        flags = appuifw.FFormViewModeOnly
        f = appuifw.Form(data, flags)
        f.execute()

def main():
    app = SportsDiaryApp()
    app.initialize_db(u"c:\\SportsDiary.db")
    app.run()

if __name__ == '__main__':
    old_title = appuifw.app.title
    try:
        appuifw.app.title = u"Sports diary"
        e32.ao_yield()
        main()
    finally:
        appuifw.app.title = old_title
