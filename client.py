import socket

import time

class Client:
	encoding = "utf-8"
	def __init__(self, ip, port):
		self._ip = ip
		self._port = port
		self._client = socket.socket()
		self._client.connect((self._ip, self._port))

	def send_recv(self, message):
		self._client.send(bytes(message, Client.encoding))
		print(self._client.recv(1024).decode(Client.encoding))

if __name__ == "__main__":
	c = Client("localhost", 9999)

		# try:
	c.send_recv("Client: Hi server! How are you buddy?")
	

		# except:
		# 	print("Error in message sending, waiting 10 seconds before trying again")
		# 	time.sleep(10)
