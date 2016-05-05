from MorseNetwork import *
from BlinkTX import BlinkTX
import RPi.GPIO as GPIO
from array import *

class PhysicalLayer():
        def __init__(self):
                self.receiver = SetPin(16,"GPIO_23",direction="RX")
                self.transmitter = BlinkTX(15,"GPIO_22",direction="TX")
                self.transmitter.turn_low()
                self.receiving = 0
                # This array will have time of the 1 and 0 transmission, alternating
                # starting with 1. You cannot put a tuple into an array, and therefore
                # I had to go with this one. Array.array instead of list is used because
                # array takes up less space and I therefore wanted something small
                self.times = array('d', []) # 'd' typecode floating point 8 byte
                self.t_start = 0

        def transmit(self):
                self.transmitter.turn_low()
                while True:
                        tuples = physicalQueueSend.get()
                        self.transmitter(tuples)


        def receive(self):
                # Everytime an interrupt happens, the callback function is
                # called in a new thread. You need to add the event detect 
                # only once, and from there it will itself create the thread
                # and destroy it.
                # Therefore, the physicalRX thread really isn't anything except
                # adding this event, and is otherwise useless and shouldn't be a
                # thread unless you want to print stars or something like that
                # while it is running
                GPIO.add_event_detect(self.receiver.headerpin, GPIO.BOTH, 
                                        callback=self.parseTime)
                while True:
                    print('***')
                    time.sleep(1)
         
        def parseTime(self, channel):
                if not self.receiving:
                    # Check if it is a beginning of a transmission (aka 1 received)
                    # If it is a 0, continue waiting.
                    if GPIO.input(self.receiver.headerpin):
                        self.receiving = 1
                        self.t_start = time.time()
                else:
                    t_received = time.time()
                    # If received the high bit EOM of 8 bits, stop receiving and
                    # put the array of stuff onto the dll queue
                    dt = t_received - self.t_start
                    self.t_start = t_received
                    if (not GPIO.input(self.receiver.headerpin)) and (
                        dt >= 7.7 / transmission_rate):
                        self.receiving = 0
                        physicalQueueRead.put(self.times[:])
                        del self.times[:]
                        return
                    self.times.append(dt)
