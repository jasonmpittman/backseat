import socket

import json

from backseat_server import server_message

from backseat_server import client_handler

import dns.resolver

import dns.reversename

from shared import asym_cryptography_handler as crypto

class TcpSocketHandler:
	encoding = "utf-8"
	msg_byte_len = 1024

	def __init__(self, ip, port, connections=10):
		self._ip = ip
		self._port = port
		self._connections = connections
		self._server = socket.socket()
		self._server.bind((self._ip, self._port))
		self._server.listen(self._connections)
		self._server_msg = server_message.ServerMessage()
		self._server_backend = client_handler.ClientHandler()
		self._crypto_module = crypto.AsymmetricCryptographyHandler()
		print("Server setup and Listening:")

	def get_FQDN(self, ip):
		print(f"|{ip}|")
		addr = dns.reversename.from_address(ip).to_text()
		res = dns.resolver.query(addr,"PTR")
		print("----------")
		print(f"|{res[0]}|")
		print("----------")
		return res[0]

	def verify_FQDN(self, FQDN):
		pass


#Add encryption!!
	def send(self, client):
		message = self._server_msg.to_json()
		cyphertext = self._crypto_module.encrypt(message)
		print(cyphertext)

		try:
			client.send(cyphertext)
			client.shutdown(socket.SHUT_WR)
		except:
			print("Server Socket error: Failed to send")

	def recieve(self, client):
		res = ""
		cyphertext = ""
		try:
			while True:
				raw_msg = client.recv(TcpSocketHandler.msg_byte_len)
				if not raw_msg:
					break
				cyphertext += raw_msg
			res = self._crypto_module.decrypt(cyphertext)
			return res


		except:
			print("Server Socket error: Failed to recieve")
			return None

	def server_loop(self):
		# Figure out a way to breakup large messages so that they can be sent and recieved without issue
		client = None
		try:
			while True:
				client, c_ip = self._server.accept()
				ip, port = c_ip
				print(f"Connected to {c_ip}")
				self.get_FQDN(ip)
				res = ""
				try:
					res = self.recieve(client)
					print(res)
					handler_result = self._server_backend.client_handler(res)

					if handler_result != None:
						command, command_id, count = handler_result
						print(f"handler_result != none: command: {command}, command_id: {command_id}, count: {count}")
						#not_ready, command, sudo, password, sequence, depot_items, command_id=0
						self._server_msg.add_data(False, command, "", "", 0, count, command_id)
						self.send(client)
						results = self.recieve(client)
						print(f"results:\n {results['stdout']}")
						handler_results = self._server_backend.client_handler(results)
						# print(results["stdout"])
						print("handler_results2:")
						print(handler_results)
					else:
						print("handler_result = None")
						# create a situation where it can return a message for the client to wait for the server
						# and the server can ping the client to wake it up

				except:
					print("Server Loop Error: Server loop failed")
				client.close()
		except KeyboardInterrupt:
			print("\n Keyboard Interupt")
			self._server.close()
			if client != None:
				print("client closed")
				client.close()
