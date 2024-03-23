"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json

from tkinter import *
import random

import base64  # for encryption and decryption

root = Tk()
root.geometry("1200x6000")
root.title("Encrypt & Decrypt Message ")
Tops = Frame(root, width=1600, relief=SUNKEN)
Tops.pack(side=TOP)

f1 = Frame(root, width=800, relief=SUNKEN)
f1.pack(side=LEFT)

lblInfo = Label(TOP, font=("Robot", 40, 'bold'), text="Secure Messaging", fg="BLACK", bd= 10, anchor= 'w')
lblInfo.grid(row=0, column=0)
Msg = StringVar()
key = StringVar()
mode = StringVar()
result = StringVar()

lblMsg = Label(f1, font=('arial', 16, 'bold'), text = "Message", bd=16, anchor='w' )
lblMsg.grid(row=1, column=0)
txtMsg = Entry(f1, font=('arial', 16, 'bold'), textvariable = Msg, bd=10, insertwidth=4, bg="powder blue", justify="right")
txtMsg.grid(row=1, column=1)

lblkey = Label(f1, font=('arial', 16, 'bold'), text = "key", bd=16, anchor='w' )
lblkey.grid(row=2, column=0)
txtkey = Entry(f1, font=('arial', 16, 'bold'), textvariable = key, bd=10, insertwidth=4, bg="powder blue", justify="right")
txtkey.grid(row=2, column=1)

lblmode = Label(f1, font=('arial', 16, 'bold'), text = "Mode(e for Enc, d for Dec", bd=16, anchor='w' )
lbmode.grid(row=3, column=0)
txtmode = Entry(f1, font=('arial', 16, 'bold'), textvariable = mode, bd=10, insertwidth=4, bg="powder blue", justify="right")
txtmode.grid(row=3, column=1)

lblResult = Label(f1, font=('arial', 16, 'bold'), text = "Result", bd=16, anchor='w' )
lblResult.grid(row=2, column=2)
txtResult = Entry(f1, font=('arial', 16, 'bold'), textvariable = result, bd=10, insertwidth=4, bg="powder blue", justify="right")
txtResult.grid(row=2, column=3)

btnTotal = Button(f1, padx=16, pady=8, bd=16, fg="black", font=('arial', 16, 'bold'), width=10, text="Show Message", bg="powder blue", command= Results).grid(row=7, column=1)

btnReset = Button(f1, padx=16, pady=8, bd=16, fg="black", font=('arial', 16, 'bold'), width=10, text="Reset", bg="powder blue", command= Reset).grid(row=7, column=2)

btnExit = Button(f1, padx=16, pady=8, bd=16, fg="black", font=('arial', 16, 'bold'), width=10, text="Exit", bg="powder blue", command= Exit).grid(row=7, column=3)

root.mainloop()
class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

        #set up base key, shared key and private key

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]


            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg


def encode(key, msg):
    enc = []
    for i in range(len(msg)):
        key_c = key[i%len(key)]
        enc_c = chr((ord(msg[i]) + ord(key_c)) %256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256+ord(enc[i])-ord(key_c)) % 256)

        dec.append(dec_c)
    return "".join(dec)


def Results():
    msg = Msg.get()
    k = key.get()
    m = mode.get()
    if m == "e":
        result.set(encode(k, msg))
    else:
        result.set(decode(k, msg))


def Reset():
    Msg.set("")
    key.set("")
    mode.set("")


def Exit():
    root.destroy()


