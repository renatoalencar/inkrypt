
class Cipher:

	CHUNK = 1024

	def __init__(self, file, keyfile):
		self.file = file
		self.keyfile = keyfile

	def __call__(self, output):
		chunk = self.file.read(self.CHUNK)
		keychunk = self.keyfile.read(self.CHUNK)

		while chunk and keychunk:
			for i in range(len(chunk)):
				output.write(self.xor(chunk[i], keychunk[i]))
			chunk = self.file.read(self.CHUNK)
			keychunk = self.keyfile.read(self.CHUNK)
	
	def xor(self, a, b):
		return chr(ord(a) ^ ord(b))
