#  ______   ______   ____ 
# |  _ \ \ / /  _ \ / ___|
# | |_) \ V /| |_) | |    
# |  __/ | | |  _ <| |___ 
# |_|    |_| |_| \_\\____|
                         

# "The Dumbest Client you've ever seen made by the dumbest person you've ever seen." A CLI IRC client programmed entirely in python with as few libraries as possible made by me, this fat guy over here.

import socket
import keyboard
import time
from multiprocessing import Process
import sys
overflow = 0

log = [""]

def on_key_event(e):
    keypressed = str({e.name}) + str ({e.event_type})
    print (keypressed)

# Define server and client information.
HOST = 'irc.libera.chat'  # IRC Server Address. (ADD FUNCTION TO SWITCH IN CLIENT DUMBASS!)
PORT = 6667
NICK = "barfpile"
IDENT = NICK
REALNAME = NICK
CHANNEL = '#test'


# Ok so what the fuck did you do (Errors on log not found)
def updatetext ():
    global log
    print(f"{"".join(log) + "                                                                                                    "}", end="\r", flush=True)

def on_key_event(e):
    global log
    if e.name == "backspace" and len(log) >= 1 and e.event_type == "down":
        log.pop(len(log) - 1)
        updatetext()
    elif e.name == "enter" and e.event_type == "down" and len(log) >= 1:
        send_message(CHANNEL, "".join(log))
        print("YOU HIT ENTER")
        log = []
    elif e.name == "space" and e.event_type == "down":
        log.append(" ")
    elif e.event_type == "down":
        if len(e.name) == 1:
            log.append(e.name)
            updatetext()
# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect((HOST, PORT))

# Send user information
s.send(f'USER {IDENT} {HOST} bla : {REALNAME}\r\n'.encode())
s.send(f'NICK {NICK}\r\n'.encode())

# Function to send messages
def send_message(channel, message):
    while overflow < sys.maxsize:
        if len(message) >= 1:
            s.send(f'PRIVMSG {channel} :{message}\r\n'.encode())
            log = [""]

# Function to join a channel
def join_channel(channel):
    s.send(f'JOIN {channel}\r\n'.encode())

# Join a channel
join_channel(CHANNEL)

def get_input():
    global overflow
    while overflow < sys.maxsize:
        keyboard.hook(on_key_event)
        keyboard.wait()
        overflow += 1


# Keep the connection alive and handle incoming messages
def maintain():
    global overflow
    while overflow < sys.maxsize:
        try:
            data = s.recv(2048).decode()
            if data.startswith('PING'):
                s.send('PONG {}\r\n'.format(data.split()[1]).encode())
            print(data)
        except socket.error:
            print("Server disconnected")
        overflow += 1

if __name__=='__main__':
    p1 = Process(target=get_input)
    p1.start()
    p2 = Process(target=maintain)
    p2.start()