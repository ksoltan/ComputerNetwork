from MorseNetwork import *
from MorseTX import MorseTX
import hashing
import random

class DataLinkLayer():
        def __init__(self):
                self.my_address = 'I'

        def transmit(self):
            while True:
                network_header, to_address, msg = networkQueueSend.get()
                transmission = self.makePackage(network_header, to_address, msg)
                #print(transmission)
                tuples = MorseTX(transmission)
                self.putOnLine(tuples)

        # Put individual packet on the line (aka place it in queue)
        def putOnLine(self, tuples):
                # check if anyone is on line transmitting
                # IsLineOpen should return 0 if cannot transmit
                # Accessing the physical layer directly because all attempts
                # at making a queu that would update the values on the line
                # did not work. The program would freeze. The queue either filled up
                # or the infinite queue wouldn't be happy.
                # I also tried a LifoQueue with the same results
                while p.receiver.read_pin():
                    # While there is something being transmitted, wait random
                    # amount of time before checking again
                    time.sleep(random.random())
                # Line is empty, can start transmitting
                physicalQueueSend.put(tuples)

        def makePackage(self, network_header, to_address, msg):
            # If the message is more than 128 characters, split it up into packages
            # HEADER: to from parity(checksum) NETWORK_HEADER
            msg_hash = hashing.getHash(msg.upper())
            # print('{0} {1} {2} {3}'.format(to_address, self.my_address, msg_hash, 
            #     network_header))
            return '{0} {1} {2} {3}'.format(to_address, self.my_address, msg_hash, 
                network_header).upper()

        def receive(self):
            while True:
                transmission = MorseRX(self.mapToStateTuples())
                self.parseWrapper(transmission)

        def mapToStateTuples(self):
            # The queue will be getting an array
            times = physicalQueueRead.get()
            for i in range(len(times)):
                # Even indeces correspond to high bit, odd correspond to 0
                yield((int(not(i % 2)), self.getDitTime(times[i])))

        def getDitTime(self, t):
            # t is in seconds. Must convert to bits based on transmission rate
            # x bits/s * s = bits. Therefore transmission_rate * t = bits
            er = 0.5
            approx_dit_time = t * transmission_rate
            bit = round(approx_dit_time)
            if abs(approx_dit_time - 1) < er:
                bit = 1
            elif abs(approx_dit_time - 3) < er:
                bit = 3
            elif abs(approx_dit_time - 7) < er:
                bit = 7
            #print("bit for t = " + str(t) + " is " + str(bit))
            return round(approx_dit_time)


        def mapToStateTuples2(self):
            # Keep taking from queue until it stops giving voltages
            # Translate them into tuples, and then from morse to letters
            er = 0.5
            num_zeros = 0 # consecutive readings
            num_ones = 0 # This function is called because a 1 was picked up on the line
    		# If there are 8 zeros, it is the end of a transmission
            while num_ones < 9 * sampling_rate:
                voltage = physicalQueueRead.get()
                #print(voltage)
                #print("Num_zeros: {0}, num_ones: {1}\n".format(num_zeros, num_ones))
                if voltage:
                # The pin reads a 1. Check to see whether there were consecutive 0s before
                    zeros = 0
                    if num_zeros != 0:
                            zeros = round(num_zeros / sampling_rate)
                    #print("Entered if voltage; zeros count: {0}\n".format(zeros))
                    # Check if this was time between 
                    if abs(zeros - 1) < er:
                            yield((0, 1))
                    elif abs(zeros - 3) < er:
                            yield((0, 3))
                    elif abs(zeros - 7) < er:
                            yield((0, 7))
                    if abs(round(num_ones / sampling_rate) - 8) < er:
                            yield((1, 8))
                            break
                    num_zeros = 0
                    num_ones += 1
                else:
                    ones = 0
                    if num_ones != 0:
                            ones = round(num_ones / sampling_rate)
                    #print("Entered else; nums count: {0}\n".format(ones))
                    if abs(ones - 1) <= er:
                            yield((1, 1))
                    elif abs(ones - 3) <= er:
                            yield((1, 3))
                    num_ones = 0
                    num_zeros += 1
                time.sleep(1 / (transmission_rate * sampling_rate))

        # TODO: adds to queue in this function. Should it?
        def parseWrapper(self, transmission):
                # Because of the choice of using spaces between pieces of the header
                # To check the checksum of the message, the dll needs to know
                # how muany things go into the header to figure out what the payloadis
                # because it needs to differentiate between what is part of the payload
                # and what is the header
                num_elem_in_net_header = 5
            # HEADER: to from parity(checksum) NETWORK_STUFF
                #print(transmission)
                if transmission == None:
                # Go back to listening
                        return 'Got nothing'
                else:
                    packet = transmission.split(' ')
                    #print(packet)
                    to_address = packet[0]
                    sent_hash = packet[2]
                    msg = ' '.join(packet[7:])
                    if to_address != self.my_address:
                        print("Not for me")
                        return
                    if hashing.getHash(msg) != sent_hash:
                        print("Error Occurred")
                        return
                    networkQueueRead.put(packet[3: 7] + [msg])
                    return msg
