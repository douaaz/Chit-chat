#!/usr/bin/env python3

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk     # ttk.Separator
import json
import hashlib # SHA-512

from chat_utils import *
import policies

import random

# python3 -m pip install emoji
#import emoji


# Documents Widget options
# https://www.tutorialspoint.com/python/python_gui_programming.htm

#https://www.nyu.edu/employees/resources-and-services/media-and-communications/nyu-brand-guidelines/designing-in-our-style/nyu-colors.html
COLOR_PRIMARY_VIOLET='#57068c'
COLOR_PRIMARY_ULTRA_VIOLET='#8900e1'
COLOR_PRIMARY_BLACK='#000000'
COLOR_SECONDARY_DEEP_VIOLET='#330662'
COLOR_SECONDARY_MEDIUM_VIOLET_1='#702b9d'
COLOR_SECONDARY_MEDIUM_VIOLET_2='#7b5aa6'
COLOR_SECONDARY_LIGHT_VIOLET_1='#ab82c5'
COLOR_SECONDARY_LIGHT_VIOLET_2='#eee6f3'
COLOR_NEUTRAL_DARK_GRAY='#404040'
COLOR_NEUTRAL_MEDIUM_GRAY_1='#6d6d6d'
COLOR_NEUTRAL_MEDIUM_GRAY_2='#b8b8b8'
COLOR_NEUTRAL_MEDIUM_GRAY_3='#d6d6d6'
COLOR_NEUTRAL_LIGHT_GRAY='#f2f2f2'
COLOR_NEUTRAL_WHITE='#ffffff'

COLOR_ACCENT_TEAL='#009b8a'
COLOR_ACCENT_MAGENTA='#fb0f78'
COLOR_ACCENT_BLUE='#59B2D1'
COLOR_ACCENT_YELLOW='#f4ec51'

BUTTON_TEXT_FONT = "Helvetica 14 bold"
INSTRUCTION_FONT = "Helvetica 10 bold"
DIALOG_ENTRY_LABEL_FONT = "Helvetica 12"
# BACKGROUND_COLOR = "#17202A"
# FOREGROUND_COLOR = "#EAECEE"


# Using NYU Traditional/Subtle Color Palette
# and Magenta as Accent color
# with the exception of using back as scrollbar activebackground

#https://www.geeksforgeeks.org/args-kwargs-python/
# This is called **kwargs
# CHAT_USERNAME_STYLE = {'pady': 2, 'padx': 10, 'bg': COLOR_SECONDARY_DEEP_VIOLET, 'fg': COLOR_ACCENT_MAGENTA, 'font': "Helvetica 13 bold"}
# TOP_BAR_STYLE = {'pady': 2, 'padx': 20, 'bg': COLOR_SECONDARY_DEEP_VIOLET, 'fg': COLOR_NEUTRAL_LIGHT_GRAY, 'font': "Helvetica 14"}

# TOP_BAR_SEPARATOR_STYLE = {'background': COLOR_PRIMARY_VIOLET}

# CHAT_LOG_STYLE = {'pady': 5, 'padx': 5, 'bd': 0, 'bg': COLOR_SECONDARY_DEEP_VIOLET, 'fg': COLOR_NEUTRAL_LIGHT_GRAY, 'highlightbackground': COLOR_SECONDARY_DEEP_VIOLET, 'insertbackground': COLOR_SECONDARY_DEEP_VIOLET, 'font': "Helvetica 13"}
# CHAT_LOG_SCROLLBAR_STYLE = {'bg': COLOR_SECONDARY_DEEP_VIOLET, 'troughcolor': COLOR_SECONDARY_LIGHT_VIOLET_1, 'activebackground': COLOR_PRIMARY_BLACK}
# # cursor pictures: https://stackoverflow.com/questions/62920953/animated-cursor-in-tkinter-python
# # insertbackground : cursor color
# CHAT_ENTRY_FIELD_STYLE = {'bg': COLOR_PRIMARY_VIOLET, 'fg': COLOR_NEUTRAL_WHITE, 'insertbackground': COLOR_NEUTRAL_WHITE, 'relief': FLAT, 'cursor': 'xterm', 'font': "Helvetica 13"}
# CHAT_INACTIVE_FRAME_STYLE = {'bg': COLOR_SECONDARY_DEEP_VIOLET}
# CHAT_INTERACTIVE_FRAME_STYLE = {'bg': COLOR_PRIMARY_VIOLET}






CHAT_USERNAME_STYLE = {'pady': 2, 'padx': 10, 'bg': COLOR_PRIMARY_VIOLET, 'fg': COLOR_NEUTRAL_LIGHT_GRAY, 'font': "Helvetica 13 bold"}
TOP_BAR_STYLE = {'pady': 2, 'padx': 20, 'bg': COLOR_PRIMARY_VIOLET, 'fg': COLOR_NEUTRAL_LIGHT_GRAY, 'font': "Helvetica 14"}

TOP_BAR_SEPARATOR_STYLE = {'background': COLOR_ACCENT_TEAL}

CHAT_LOG_STYLE = {'pady': 5, 'padx': 5, 'bd': 0, 'bg': COLOR_NEUTRAL_WHITE, 'fg': COLOR_PRIMARY_BLACK, 'highlightbackground': COLOR_SECONDARY_DEEP_VIOLET, 'insertbackground': COLOR_SECONDARY_DEEP_VIOLET, 'font': "Helvetica 13"}
CHAT_LOG_SCROLLBAR_STYLE = {'bg': COLOR_NEUTRAL_MEDIUM_GRAY_2, 'troughcolor': COLOR_NEUTRAL_LIGHT_GRAY, 'activebackground': COLOR_NEUTRAL_MEDIUM_GRAY_3}
# cursor pictures: https://stackoverflow.com/questions/62920953/animated-cursor-in-tkinter-python
# insertbackground : cursor color
CHAT_ENTRY_FIELD_STYLE = {'bg': COLOR_SECONDARY_MEDIUM_VIOLET_2, 'fg': COLOR_NEUTRAL_WHITE, 'insertbackground': COLOR_NEUTRAL_WHITE, 'relief': FLAT, 'cursor': 'xterm', 'font': "Helvetica 13"}
CHAT_INACTIVE_FRAME_STYLE = {'bg': COLOR_NEUTRAL_WHITE}
CHAT_INTERACTIVE_FRAME_STYLE = {'bg': COLOR_SECONDARY_MEDIUM_VIOLET_2}
CHAT_BUTTONS_STYLE = {'bg': COLOR_SECONDARY_MEDIUM_VIOLET_2, 'fg': "black", 'activebackground': COLOR_SECONDARY_MEDIUM_VIOLET_2, 'activeforeground': "black", 'highlightcolor':'green'}



APP_NAME = "Chit-Chat"
SPLASH_SCREEN_SHOW_TIME = 3000 # ms

SPLASH_IMAGE        = 'Chit-Chat_720.gif'
APP_ICON            = 'Chit-Chat_icon_48.gif'
APP_NAME_IMAGE      = 'Chit-Chat-Text_light_gray_32h.png'
APP_DIALOG_LOGO     = 'Chit-Chat_320.gif'

WINDOW_BACKGROUND_COLOR = COLOR_PRIMARY_BLACK

# https://www.youtube.com/watch?v=LTVvHObxc4E&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=139
class SplashScreen(Tk):
    def __init__(self, callback):
        Tk.__init__(self)

        # hide the title bar
        # self.overrideredirect(False)
        # self.overrideredirect(True)
        self.attributes("-type","splash")
        self.image = PhotoImage(file=SPLASH_IMAGE)
        Label(self, image=self.image).pack()
        self.after(SPLASH_SCREEN_SHOW_TIME, lambda: callback(self))

        self.resizable(False, False)

        # https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))

        self.mainloop()

class PasswordEntry(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.entry = Entry(self, show='*')
        self.entry.pack(fill=BOTH, expand=Y, side=LEFT)
        self.entry.bind('<FocusOut>', lambda e: self.hide())

        # store image to prevent garbage collection (https://stackoverflow.com/questions/22200003/tkinter-button-not-showing-image)
        self.show_image = PhotoImage(file='show_24.png')
        self.hide_image = PhotoImage(file='hide_24.png')
        self.hideShowButton = Button(self)
        self.hide()
        self.hideShowButton.pack(side=RIGHT, fill=Y)

    def show(self):
        self.hideShowButton.configure(image=self.hide_image, command=lambda: self.hide())
        self.entry.configure(show='')
        self.entry.focus_set()

    def hide(self):
        self.hideShowButton.configure(image=self.show_image, command=lambda: self.show())
        self.entry.configure(show='*')

    def focus_set(self):
        self.entry.focus_set()

    def get(self):
        return self.entry.get()

    def bind(self, event, callback):
        self.entry.bind(event, lambda e: callback(e))


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        
        # hides the window
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

        self.icon = PhotoImage(file = APP_ICON)
        self.Window.iconphoto(True, self.icon)

        self.Window.title(APP_NAME)
        self.Window.configure(bg = WINDOW_BACKGROUND_COLOR)

    def login(self, username, password):
        self.login = Toplevel(self.Window)
        self.login.title(APP_NAME + " Login")

        frame = Frame(self.login)
        rightColumn = Frame(frame)
        leftColumn = Frame(frame)

        frame.pack(fill=X)
        self.image = PhotoImage(file = APP_DIALOG_LOGO)
        Label(frame, image=self.image).pack(side=TOP, padx=5, pady=5)

        self.loginDialogInstructions = Label(frame, text="Enter your credentials to login", font = INSTRUCTION_FONT)
        self.loginDialogInstructions.pack(side=TOP, padx=5, pady=5)

        leftColumn.pack(side=LEFT, padx=5, pady=5)
        rightColumn.pack(side=RIGHT, expand=YES, fill=X, padx=5, pady=5)
        
        Label(leftColumn, text='Name', font=DIALOG_ENTRY_LABEL_FONT).pack(side=TOP, fill='both')
        self.entryName = Entry(rightColumn)
        self.entryName.pack(side=TOP, fill=X)
        self.entryName.bind('<Return>', lambda e: self.passwordField.focus_set())

        Label(leftColumn, text='Password', font=DIALOG_ENTRY_LABEL_FONT).pack(side=TOP, fill='both')
        self.passwordField = PasswordEntry(rightColumn)
        self.passwordField.pack(side=TOP, fill=X)
        self.passwordField.bind('<Return>', lambda e: loginButton.focus_set())

        loginButton = Button(self.login, text='Login', font=BUTTON_TEXT_FONT)
        loginButton.configure(command=(lambda: self.goAhead(self.entryName.get(), self.passwordField.get())))

        loginButton.pack(side=LEFT, fill='both', padx=5, pady=5)
        loginButton.bind('<Return>', lambda e: self.goAhead(self.entryName.get(), self.passwordField.get()))
        Button(self.login, text='Register', font=BUTTON_TEXT_FONT,
                command=(lambda: self.showRegisterDialog())).pack(side=RIGHT, fill='both', padx=5, pady=5)

        self.login.resizable(False, False)

        # this is for testing and demo, auto login
        # username and password is given as arguments at staring the chat client
        if username != None and password != None:
            self.goAhead(username, password)                      
        else:
            self.login.protocol("WM_DELETE_WINDOW", lambda arg=self.Window: arg.destroy())
            self.entryName.focus_set()

        self.Window.mainloop()

    def encryptPassword(self, password):
        # salt is hard coded, full password protection is done on server side
        # cannot be hacked from the outside as the client-server connection is encrypted too
        # But we want to complicate the server-side access to the password by regular employees
        # no plain text password
        salt = b'\xddU\xca\x14\x00:\xb0\xd5\xabS\x91\xd8\xe7w\x11\n\xd7\x965\x00\x85\xf1\x8f\xb13\xef\xd2|\x08\x13Jt\x8e"\x85\x90\xb0Q\n$\xbb\xc2\x0b\xe7V\x8a\xfd\xf3S}$Ay|\xb8\xfcnx\x07\x04m\xf0\xf9\xe2'

        salted = salt[:32] + password.encode() + salt[33:]
        return hashlib.sha512(salted).hexdigest()

    def handleRegisterButton(self, name, password, confirmPassword):
        if password == confirmPassword:
            result = policies.isUserNameCompliant(name)
            if result[0]:
                if policies.isPasswordCompliant(password):
                    encryptedPassword = self.encryptPassword(password)
                    msg = json.dumps({"action": "register", "name": name, "password": encryptedPassword})
                    self.send(msg)
                    print("message send")
                    response = json.loads(self.recv())
                    print(f"message received: {response}")
                    if response["status"] == 'ok':
                        self.registerDialog.destroy()
                        # set name field in Login dialog
                        self.entryName.delete(0, END)
                        self.entryName.insert(END, name)
                        # focus Password field
                        self.passwordField.focus_set()

                    else:
                        self.registryDialogInstructions.configure(text=response["message"], fg='red')
                else:
                    self.registryDialogInstructions.configure(text="Password does not comply with policy", fg='red')
            else:
                self.registryDialogInstructions.configure(text=result[1], fg='red')
        else:
            self.registryDialogInstructions.configure(text="Passwords do not match", fg='red')

    def showRegisterDialog(self):
        self.registerDialog = Toplevel()
        self.registerDialog.title("Register New User")
        frame = Frame(self.registerDialog)
        rightColumn = Frame(frame)
        leftColumn = Frame(frame)

        frame.pack(fill=X)

        self.registryDialogInstructions = Label(frame, text="Create a name password combination", font = INSTRUCTION_FONT)
        self.registryDialogInstructions.pack(side=TOP, padx=5, pady=5)
        leftColumn.pack(side=LEFT, padx=5, pady=5)
        rightColumn.pack(side=RIGHT, expand=YES, fill=X, padx=5, pady=5)
        
        Label(leftColumn, text='Name', font=DIALOG_ENTRY_LABEL_FONT).pack(side=TOP, fill='both')
        name = Entry(rightColumn)
        name.pack(side=TOP, fill=X)
        name.bind('<Return>', lambda e: password.focus_set())

        Label(leftColumn, text='Password', font=DIALOG_ENTRY_LABEL_FONT).pack(side=TOP, fill='both')
        password = PasswordEntry(rightColumn)
        password.pack(side=TOP, fill=X)
        password.bind('<Return>', lambda e: confirmPassword.focus_set())

        Label(leftColumn, text='Confirm password', font=DIALOG_ENTRY_LABEL_FONT).pack(side=TOP, fill='both')
        confirmPassword = PasswordEntry(rightColumn)
        confirmPassword.pack(side=TOP, fill=X)
        confirmPassword.bind('<Return>', lambda e: registerButton.focus_set())

        registerButton = Button(self.registerDialog, text='Register', font=BUTTON_TEXT_FONT, 
                command=lambda: self.handleRegisterButton(name.get(), password.get(), confirmPassword.get()))
        registerButton.pack(side=LEFT, fill='both', padx=5, pady=5)
        registerButton.bind('<Return>', lambda e: self.handleRegisterButton(name.get(), password.get(), confirmPassword.get()))
        Button(self.registerDialog, text='Cancel', font=BUTTON_TEXT_FONT,
                    command=(lambda: self.registerDialog.destroy())) \
                        .pack(side=RIGHT, fill='both', padx=5, pady=5)

        self.registerDialog.resizable(False, False)
        name.focus_set()


    def goAhead(self, name, password):
        if len(name) > 0:
            encryptedPassword = self.encryptPassword(password)
            msg = json.dumps({"action": "login", "name": name, "password": encryptedPassword})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.enterText("Hello " + self.name + "!\n\n")# + menu + "\n")
            else:
                self.loginDialogInstructions.configure(text= response['status'], fg="red")
                return 

            # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()
        


        # self.Window.geometry("560x600")
        # self.Window.minsize(height=560, width=560)
        
        # User name Right Aligned
        heading = Frame(self.Window)
        heading.pack(side=TOP, fill=X)
        
        self.text_logo = PhotoImage(file=APP_NAME_IMAGE)

        Label(heading, image=self.text_logo, **TOP_BAR_STYLE).pack(side=LEFT, fill=BOTH, ipadx=10)
        Label(heading, **TOP_BAR_STYLE).pack(side=LEFT, fill=BOTH, expand=1)
        Label(heading, text=self.name, **CHAT_USERNAME_STYLE).pack(side=LEFT, fill=BOTH)

        # https://pythonguides.com/python-tkinter-separator       
        style = ttk.Style()
        style.configure('blue.TSeparator', **TOP_BAR_SEPARATOR_STYLE)
        separator = ttk.Separator(self.Window, orient='horizontal', takefocus=0, style='blue.TSeparator')
        separator.pack(side=TOP, fill=X, ipady=1)

        interactive = Frame(self.Window)
        interactive.pack(side=BOTTOM, fill=X)#, expand=1)

        # main= Frame(interactive, **CHAT_INTERACTIVE_FRAME_STYLE)
        # main.pack(side=TOP, fill=BOTH)
        # self.timeButton = Button(main, text="time",**CHAT_BUTTONS_STYLE)
        # self.timeButton.pack(side=LEFT, expand=1)
        # whoButton= Button(main, text="who")
        # whoButton.pack(side=LEFT, expand=1)
        # Button(main, text="connect").pack(side=LEFT, expand=1)
        # Button(main, text="sonnet").pack(side=LEFT, expand=1)
        # Button(main, text="feeling happy").pack(side=LEFT, expand=1)
        # Button(main, text="emoji").pack(side=LEFT, expand=1)
        # Button(main, text="leave").pack(side=LEFT, expand=1)




        buttonbar = Frame(interactive)
        buttonbar.pack(side=TOP, fill=X)#, expand=1)
        self.timeButton = Button(buttonbar, text='Time', **CHAT_BUTTONS_STYLE, command=lambda: self.command('time'))
        self.timeButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.whoButton = Button(buttonbar, text='Who', **CHAT_BUTTONS_STYLE, command=lambda: self.command('who'))
        self.whoButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.connectButton = Button(buttonbar, text='Connect', **CHAT_BUTTONS_STYLE, command=lambda: self.connectCommand())
        self.connectButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.sonnetButton = Button(buttonbar, text='Sonnet', **CHAT_BUTTONS_STYLE, command=lambda: self.sonnetCommand())
        self.sonnetButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.iAmHappyButton = Button(buttonbar, text='Feeling happy', **CHAT_BUTTONS_STYLE, command=lambda: self.command('p' + str(random.randint(1,154))))
        self.iAmHappyButton.pack(side=LEFT, fill=BOTH, expand=1)
        # self.emojiButton = Button(buttonbar, text='Emoji')
        # self.emojiButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.leaveButton = Button(buttonbar, text='Leave', **CHAT_BUTTONS_STYLE, command=lambda: self.byeCommand())
        self.leaveButton.pack(side=LEFT, fill=BOTH, expand=1)

        # The text input field
        self.entryMsg = Entry(interactive, **CHAT_ENTRY_FIELD_STYLE)
        self.entryMsg.pack(side=BOTTOM, fill=BOTH, expand=1, pady=2, padx=2)

        main = Frame(self.Window, **CHAT_INACTIVE_FRAME_STYLE)
        main.pack(side=TOP, fill=BOTH, expand=1)

        scrollbar = Scrollbar(main, **CHAT_LOG_SCROLLBAR_STYLE)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.textCons = Text(main, yscrollcommand=scrollbar.set, **CHAT_LOG_STYLE)
        self.textCons.pack(side=LEFT, fill=Y)
        scrollbar.config(command=self.textCons.yview)

        self.entryMsg.focus()
        self.sm.setStateChangeCallback(lambda s: self.newState(s))


    def layout2 (self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()

        self.Window.geometry("560x600")
        self.Window.minsize(height=560, width=560)
        
        # User name Right Aligned
        heading = Frame(self.Window)
        heading.pack(side=TOP, fill=X)
        
        self.text_logo = PhotoImage(file=APP_NAME_IMAGE)

        Label(heading, image=self.text_logo, **TOP_BAR_STYLE).pack(side=LEFT, fill=BOTH, ipadx=10)
        Label(heading, **TOP_BAR_STYLE).pack(side=LEFT, fill=BOTH, expand=1)
        Label(heading, text=self.name, **CHAT_USERNAME_STYLE).pack(side=LEFT, fill=BOTH)

        # https://pythonguides.com/python-tkinter-separator       
        style = ttk.Style()
        style.configure('blue.TSeparator', **TOP_BAR_SEPARATOR_STYLE)
        separator = ttk.Separator(self.Window, orient='horizontal', takefocus=0, style='blue.TSeparator')
        separator.pack(side=TOP, fill=X, ipady=1)

        interactive = Frame(self.Window, **CHAT_INTERACTIVE_FRAME_STYLE)
        interactive.pack(side=BOTTOM, fill=X)#, expand=1)

        buttonbar = Frame(interactive, **CHAT_INTERACTIVE_FRAME_STYLE)
        buttonbar.pack(side=TOP, fill=X, expand=1)
        self.timeButton = Button(buttonbar, text='Time', command=lambda: self.command('time'))
        self.timeButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.whoButton = Button(buttonbar, text='Who', command=lambda: self.command('who'))
        self.whoButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.connectButton = Button(buttonbar, text='Connect', command=lambda: self.connectCommand())
        self.connectButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.sonnetButton = Button(buttonbar, text='Sonnet', command=lambda: self.sonnetCommand())
        self.sonnetButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.iAmHappyButton = Button(buttonbar, text='Feeling happy', command=lambda: self.command('p' + str(random.randint(1,154))))
        self.iAmHappyButton.pack(side=LEFT, fill=BOTH, expand=1)
        # self.emojiButton = Button(buttonbar, text='Emoji')
        # self.emojiButton.pack(side=LEFT, fill=BOTH, expand=1)
        self.leaveButton = Button(buttonbar, text='Leave', command=lambda: self.byeCommand())
        self.leaveButton.pack(side=LEFT, fill=BOTH, expand=1)

        # The text input field
        self.entryMsg = Entry(interactive, **CHAT_ENTRY_FIELD_STYLE)
        self.entryMsg.pack(side=BOTTOM, fill=BOTH, expand=1, pady=2, padx=2)

        main = Frame(self.Window, **CHAT_INACTIVE_FRAME_STYLE)
        main.pack(side=TOP, fill=BOTH, expand=1)

        scrollbar = Scrollbar(main, **CHAT_LOG_SCROLLBAR_STYLE)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.textCons = Text(main, yscrollcommand=scrollbar.set, **CHAT_LOG_STYLE)
        self.textCons.pack(side=LEFT, fill=Y)
        scrollbar.config(command=self.textCons.yview)

        self.entryMsg.focus()
        self.sm.setStateChangeCallback(lambda s: self.newState(s))

        #                         text="\U0001F600\U0001F923\U0001F920", #"Send",


    def newState(self, newState):
        if newState == S_CHATTING:
            self.timeButton.configure(state=DISABLED)
            self.whoButton.configure(state=DISABLED)
            self.connectButton.configure(state=DISABLED)
            self.sonnetButton.configure(state=DISABLED)
            self.iAmHappyButton.configure(state=DISABLED)
            # self.emojiButton.configure(state=ACTIVE)
            self.leaveButton.configure(state=ACTIVE)
            self.entryMsg.bind('<Return>', lambda e: self.sendText())
        else:
            self.timeButton.configure(state=ACTIVE)
            self.whoButton.configure(state=ACTIVE)
            self.connectButton.configure(state=ACTIVE)
            self.sonnetButton.configure(state=ACTIVE)
            self.iAmHappyButton.configure(state=ACTIVE)
            # self.emojiButton.configure(state=DISABLED)
            self.leaveButton.configure(state=DISABLED)
            self.entryMsg.bind('<Return>', lambda e: None)

    def enterText(self, msg):
        if len(msg) > 0:
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, msg)
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)

    def sendText(self):
        # get message and clear the entry field
        msg = self.entryMsg.get().rstrip()
        self.entryMsg.delete(0, END)

        # send message to server and client display
        if len(msg) > 0:
            self.my_msg = msg
            self.enterText(msg)

    def command(self, message):
        if len(message) > 0:
            self.my_msg = message

    def byeCommand(self):
        self.command('bye')
        self.enterText('bye\n')

    def connectCommand(self):
        name = self.entryMsg.get().rstrip()
        if name != '':
            self.entryMsg.delete(0, END)
            command = 'c ' + name  
            self.command(command)

    def sonnetCommand(self):
        number = self.entryMsg.get().rstrip()
        if number != '':
            self.entryMsg.delete(0, END)
            command = 'p' + number  
            self.command(command)

    # function to basically start the thread for sending messages
    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.enterText(self.system_msg + "\n")

    def run(self, name, password):
        self.login(name, password)


# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
