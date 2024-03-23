import socket
import ssl
import sys
from chat_utils import *
import client_state_machine as csm
from GUI import *


class Client:
    def __init__(self, args):
        self.args = args

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def init_chat(self):
        # https://docs.python.org/3/library/ssl.html#socket-creation
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations(SERVER_CERT)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = self.context.wrap_socket(s, server_side=False, server_hostname=SERVER_HOSTNAME)
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        try:
            self.socket.connect(svr)
        except: 
            print("Server Unavailable")
            exit()
        self.sc = SplashScreen(self.destroySplash)

    def destroySplash(self, splashscreen):
        splashscreen.destroy()
        sm = csm.ClientSM(self.socket)
        self.gui = GUI(self.send, self.recv, sm, self.socket)
        self.gui.run(None if self.args.n == None else self.args.n, None if self.args.p == None else self.args.p)
        print("gui is off")
        self.quit()

    # def shutdown_chat(self):
    #     return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def run_chat(self):
        self.init_chat()
