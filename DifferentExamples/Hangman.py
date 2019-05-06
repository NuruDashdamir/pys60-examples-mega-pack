
import inbox, messaging, appuifw, e32, contacts

current_word = None
guessed = None
num_guesses = 0
def new_game():
    global current_word, guessed, num_guesses
    word = appuifw.query(u"Word to guess", "text")
    if word:
         current_word = word.lower()
         guessed = list("_" * len(current_word))
         num_guesses = 0
         print "New game started. Waiting for messages..."

def game_status():
    if current_word:
         appuifw.note(u"Word to guess: %s\n" % current_word +\
                       "Current guess: %s\n" % "".join(guessed) +\
                       "Number of gusses: %d" % num_guesses)
    else:
         appuifw.note(u"Game has not been started")  

def quit():
    print "HANGMAN SERVER EXITS"
    app_lock.signal()


def find_number(sender):
        cdb = contacts.open()
        matches = cdb.find(sender)
        if matches:
                num = matches[0].find("mobile_number")
                if num:
                        return num[0].value
                else:
                        return None
        return sender

def message_received(msg_id):
     global guessed, num_guesses
     box = inbox.Inbox()
     msg = box.content(msg_id).lower()
     sender = box.address(msg_id)
     box.delete(msg_id)

     print "Message from %s: %s" % (sender, msg)     

     if current_word == None:
          return

     elif msg.startswith("guess") and len(msg) >= 7:
          guess = msg[6]
          for i in range(len(current_word)):
               if current_word[i] == guess:
                    guessed[i] = guess
          num_guesses += 1

     elif msg.startswith("word"):
          if msg[5:] == current_word:
               appuifw.note(u"%s guessed the word!" % sender)
               guessed = list(current_word)

     num = find_number(sender)
     if num:
             messaging.sms_send(num, u"Status after %d guesses: %s" %\
                (num_guesses, "".join(guessed)))


box = inbox.Inbox()
box.bind(message_received)

appuifw.app.exit_key_handler = quit
appuifw.app.title = u"Hangman Server"
appuifw.app.menu = [(u"New Game", new_game),
                    (u"Game Status", game_status)]

print "HANGMAN SERVER STARTED"
print "Select 'Options -> New Game' to initialize a new game"

app_lock = e32.Ao_lock()
app_lock.wait()
