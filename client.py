import socket

import time

import client_message

import json

class Client:
	encoding = "utf-8"
	def __init__(self, ip, port):
		self._ip = ip
		self._port = port
		self._client = socket.socket()

			# more resilience needs to be built into the program for things like this
		self._client_msg = client_message.ClientMessage()

	def connect(self):
		#this needs to be moved into its own function
		try:
			self._client.connect((self._ip, self._port))
			return True
		except:
			print("Cannot connect to server, server is probably off")
			return False

	def send_recv(self, message="Test"):
		res = ""
		# self._client_msg.add_data(ready, completed, stdout, stderr, successful, exit_code)
		self._client_msg.add_data(True, True, message, "", True, 0)
		message = self._client_msg.to_json()
		try:
			self._client.send(bytes(message, Client.encoding))
			res = self._client.recv(1024).decode(Client.encoding)
			res = json.loads(res)
		except:
			#this is for testing purposes only
			res = {"command": None}

		return res

	def send_results(self, results):
		self._client_msg.add_data(True, True, results, "", True, 0)
		message = self._client_msg.to_json()
		try:
			self._client.send(bytes(message, Client.encoding))
			res = self._client.recv(1024).decode(Client.encoding)
			print(res)
		except:
			print("send_results: Failed")

if __name__ == "__main__":
	c = Client("localhost", 9999)

		# try:
	c.connect()
	c.send_recv("")


		# except:
		# 	print("Error in message sending, waiting 10 seconds before trying again")
		# 	time.sleep(10)
