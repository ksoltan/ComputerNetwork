from MorseNetwork import *

class ApplicationLayer():
    def __init__(self):
        self.me = 1

    def transmit(self):
        while True:
            to = input("TO: ")
            msg = input("MESSAGE TO SEND: ")
            if not msg:
                continue
            elif msg.upper() == "QUIT":
                return
            else:
                applicationQueueSend.put(('I', msg))

    def receive(self):
        while True:
            from_address, msg = applicationQueueRead.get()
            print("From: " + str(from_address) + "\n" + str(msg))