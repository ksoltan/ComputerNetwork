from MorseNetwork import *
from MorseCode import MorseCode

class NetworkLayer():
	def __init__(self):
		self.address = 'I'
		self.global_ip = 'I'
		self.payload_len = 100
	
	def receive(self):
		# Getting the information DLL parses
		# Figuring out where it goes
		# HEADER: to from messageNumber numOfMessages payload
		while True:
			to_address, from_address, msg_num, num_msgs, payload = networkQueueRead.get()
			#print("{0} {1} {2} {3} {4}".format(to_address, from_address, msg_num, num_msgs, payload))
			## Collect all of the packets and pass up to the application
			##TODO:
			applicationQueueRead.put((from_address, payload))

	def transmit(self):
		# Gets info from the application
		# TODO: SPLIT INTO MESSAGES
		# HEADER:  DATALINKSTUFF to from messageNumber numOfMessages payload

		while True:
			to_address, payload = applicationQueueSend.get()
			networkQueueSend.put(('{0} {1} {2} {3} {4}'.format(to_address,
					self.global_ip, 1, 1, payload), to_address, payload))

	def getNumDitsInChar(self, c):
		num_dits = 0
		for d in MorseCode[c.upper()]:
			num_dits += 1 if d == '.' else 0
		return num_dits

	def splitIntoPackets(self, msg):
		packets = []
		start = 0
		i = 0
		num_dits = 0
		while i < len(msg):
			num_dits_c = getNumDitsInChar(msg[i])
		return packets
