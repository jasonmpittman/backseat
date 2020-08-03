import socket

import time

import client_message

class Client:
	encoding = "utf-8"
	def __init__(self, ip, port):
		self._ip = ip
		self._port = port
		self._client = socket.socket()
		try:
			self._client.connect((self._ip, self._port))
		except:
			print("Cannot connect to server, server is probably off")
			print("Exiting program")
			exit(1)
			# more resilience needs to be built into the program for things like this
		self._client_msg = client_message.ClientMessage()

	def send_recv(self, message):
		res = ""
		# self._client_msg.add_data(ready, completed, stdout, stderr, successful, exit_code)
		self._client_msg.add_data(True, True, "woo output", "", True, 0)
		message = self._client_msg.to_json()
		try:
			self._client.send(bytes(message, Client.encoding))
			res = self._client.recv(1024).decode(Client.encoding)
		except:
			res = ""

		print(res)

if __name__ == "__main__":
	c = Client("localhost", 9999)

		# try:
	c.send_recv("")


		# except:
		# 	print("Error in message sending, waiting 10 seconds before trying again")
		# 	time.sleep(10)
