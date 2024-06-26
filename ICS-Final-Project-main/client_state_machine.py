"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
from diffie_hellman import DiffieHellman

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.diffieHellman = DiffieHellman()
        self.stateChanged = lambda s: None  # Do nothing 

    def setStateChangeCallback(self, callback):
        self.stateChanged = callback
        self.stateChanged(self.state)

    def set_state(self, state):
        self.state = state
        self.stateChanged(state)

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
            # the server has created the connection between the both clients
            # now we create Client to Client secure messaging
            if self.diffieHellman.createSharedSecret(self.s, self.me):
                self.out_msg += 'You are connected with '+ self.peer + '\n'
                return True
            else:
                print("DiffieHellman failed")      
                return False

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

                if my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in.rstrip()

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.set_state(S_CHATTING)
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                # elif my_msg[0] == '?':
                #     term = my_msg[1:].strip()
                #     mysend(self.s, json.dumps({"action":"search", "target":term}))
                #     search_rslt = json.loads(myrecv(self.s))["results"].strip()
                #     if (len(search_rslt)) > 0:
                #         self.out_msg += search_rslt + '\n\n'
                #     else:
                #         self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem.rstrip() + '\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n'

                else:
                    # self.out_msg += menu
                    pass

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]

                    # the server has created the connection between the both clients
                    # now we create Client to Client secure messaging
                    if self.diffieHellman.createSharedSecret(self.s, self.me):
                        self.set_state(S_CHATTING)
                        self.out_msg += 'Request from ' + self.peer + '\n'
                        self.out_msg += 'You are connected with ' + self.peer
                        self.out_msg += '. Chat away!\n'
                    else:
                        print("DiffieHellman failed")      
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                encrypted_msg = self.diffieHellman.encrypt(my_msg)
                mysend(self.s, json.dumps({"action": "exchange", "from":"[" + self.me + "] ", "message": encrypted_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.set_state(S_LOGGEDIN)
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"






                elif peer_msg["action"] == "disconnect":
                    self.set_state(S_LOGGEDIN)
                else: # {"action": "exchange"}
                    decrypted_msg = self.diffieHellman.decrypt(peer_msg["message"])
                    self.out_msg += peer_msg["from"] + decrypted_msg 


            # Display the menu again
            # if self.state == S_LOGGEDIN:
            #     self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
