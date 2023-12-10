from threading import Thread
from time import sleep

tt = 9
def me():
    while True:
        print(tt)
        sleep(5)

def you():
    while True:
        print('yes')
        sleep(10)
        
# Send the email in a separate thread
msg = 'proceed now'
mg = '!'
thr = Thread(target=me)
thr.start()

you()