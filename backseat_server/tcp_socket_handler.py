import socket

import json

from backseat_server import server_message

from backseat_server import client_handler

import dns.resolver
import dns.reversename
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
		print("Server setup and Listening:")

	def get_FQDN(self, ip):
		ip = "8.8.4.4"
		print(f"|{ip}|")
		addr = dns.reversename.from_address(ip).to_text()
		res = dns.resolver.query(addr,"PTR")
		print("----------")
		print(f"|{res[0]}|")
		print("----------")
#Add encryption!!
	def send(self, client):
		message = self._server_msg.to_json() + "`"
		try:
			client.send(bytes(message, TcpSocketHandler.encoding))
		except:
			print("Server Socket error: Failed to send")

	def recieve(self, client):
		raw_res = " "
		try:
			while raw_res[-1] != "`":
				if raw_res == " ":
					raw_res = ""
				raw_res += client.recv(TcpSocketHandler.msg_byte_len).decode()
			res = raw_res.replace("`", "")
			dict_res = json.loads(res)
			return dict_res
		except:
			print("Server Socket error: Failed to recieve")
			return {}

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
