
import messaging

PHONE_NUMBER = "+10987654321"
songs = (1, 3, 9, 11)
singers = "Tori, Kate, Alanis"

for song in songs:
     for singer in singers.split(','):
          msg = u"VOTE %d %s" % (song, singer.strip())
          print "Sending SMS", msg
          messaging.sms_send(PHONE_NUMBER, msg)
