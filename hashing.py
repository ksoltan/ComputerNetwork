def getHash(msg):
	s = 0
	for c in msg:
		s += ord(c.upper())
	return chr(65 + s % 26)
#print(getHash('Hello'))
