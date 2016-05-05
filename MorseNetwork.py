from MorseRX import MorseRX
from SetPin import SetPin
import time
import queue
import threading

dit_time = 0.002
transmission_rate = 1 / dit_time
#transmission_rate = 40/3 #bits per second (0.075 s per bit)
sampling_rate = 25 # per second

# Queue into which physical layer writes values and data link reads them from
physicalQueueRead = queue.Queue(1000)
# Queue into which data link writes values and physical layer reads them from
physicalQueueSend = queue.Queue(1000)


# Queue to put dictionaries of info for packet between Network and DLL
networkQueueRead = queue.Queue(1000)
networkQueueSend = queue.Queue(1000)

applicationQueueRead = queue.Queue(100)
applicationQueueSend = queue.Queue(100)

from PhysicalLayer import PhysicalLayer
p = PhysicalLayer()

from DataLinkLayer import DataLinkLayer
dll = DataLinkLayer()

from NetworkLayer import NetworkLayer
n = NetworkLayer()

from ApplicationLayer import ApplicationLayer
a = ApplicationLayer()