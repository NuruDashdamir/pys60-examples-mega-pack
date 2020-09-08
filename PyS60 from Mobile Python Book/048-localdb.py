
import e32dbm

DB_FILE = u"c:\\python\\test.db"

def write_db():
        db = e32dbm.open(DB_FILE, "cf")
        db[u"host"] = u"www.google.com"
        db[u"port"] = u"80"
        db[u"username"] = u"musli"
        db[u"password"] = u"my secret"
        db.close()

def read_db():
        db = e32dbm.open(DB_FILE, "r")
        for key, value in db.items():
                print "KEY", key, "VALUE", value
        db.close()

print "Writing db.."
write_db()
print "Reading db.."
read_db()
