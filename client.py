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

	def send_recv(self, message=""):
		res = ""
		# self._client_msg.add_data(self, whoami, ping, ready, completed, stdout, stderr, successful, exit_code, command_id=0
		self._client_msg.add_data("localhost", True, True, message, "", True, 0)
		message = self._client_msg.to_json()

		try:
			self._client.send(bytes(message, Client.encoding))
			res = self.recieve()
			res = json.loads(res)
		except:
			#this is for testing purposes only
			res = None

		return res

	def get_command(self):
		#whoami, ping, ready, completed, stdout, stderr, successful, exit_code, command_id=0
		self._client_msg.add_data("localhost", True, True, True,"", "", False, 0)
		self.send()
		res = self.recieve()
		if res == None:
			print("get_command failed")
			return None
		else:
			return res


#Add encrpytion!!!
	def send(self):
		message = self._client_msg.to_json()
		try:
			self._client.send(bytes(message, Client.encoding))
		except:
			print("Failed to send")

	def recieve(self):
		try:
			raw_res = self._client.recv(4096).decode(Client.encoding)
			dict_res = json.loads(raw_res)
			return dict_res
		except:
			print("Failed to recieve")
			return None

	def send_results(self, command_id, stdout, stderr=""):
		# whoami, ping, ready, completed, stdout, stderr, successful, exit_code, command_id=0
		self._client_msg.add_data("localhost", False, True, True, stdout, stderr, True, 0)
		message = self._client_msg.to_json()
		try:
			self._client.send(bytes(message, Client.encoding))
			# res = self._client.recv(4096).decode(Client.encoding)
			# print(res)
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
