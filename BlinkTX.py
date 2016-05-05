#
## Lab 2.2 - Physical Layer  - Send Tuples as blinks
#
from MorseNetwork import *
from MorseTX import MorseTX
from SetPin import SetPin
import time

class BlinkTX(SetPin):
    def __init__(self,headerpin,BCM,direction="TX"):
        if direction != "TX":
            raise ValueError("direction must be 'TX'")
        super().__init__(headerpin,BCM,direction="TX")
    def __call__(self,tups):
        self.turn_low()
        for state,direction in tups:
            self.blinkTX(state,direction)
        print("Finished transmitting")
        self.turn_low()

    def blinkTX(self,state,duration):
        #print(state,duration)
        self.turn_high() if state else self.turn_low()
        time.sleep(duration / transmission_rate)

if __name__ == "__main__":
    with BlinkTX(15,"GPIO_22",direction="TX") as blink:
        while True:
            msg = input("MESSAGE TO SEND (EMPTY ENTRY YIELDS RANDOM QUOTE) :")
            if not msg:
                continue
            elif msg.upper() == "QUIT":
                break
            else:
                blink(MorseTX(msg.upper()))
