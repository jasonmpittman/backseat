import socket

import server_message

import json

import server_backend

class Server:
	encoding = "utf-8"

	def __init__(self, ip, port, connections=10):
		self._ip = ip
		self._port = port
		self._connections = connections
		self._server = socket.socket()
		self._server.bind((self._ip, self._port))
		self._server.listen(self._connections)
		self._server_msg = server_message.ServerMessage()
		self._server_backend = server_backend.ServerBackend()
		print("Server setup and Listening:")

#Add encryption!!
	def send(self, client):
		message = self._server_msg.to_json()
		try:
			client.send(bytes(message, Server.encoding))
		except:
			print("Server: Failed to send")

	def recieve(self, client):
		try:
			raw_res = client.recv(1024).decode()
			dict_res = json.loads(raw_res)
			return dict_res
		except:
			print("Server: Failed to recieve")
			return {}

	def server_loop(self):
		client = None
		try:
			while True:
				client, c_ip = self._server.accept()
				print(f"Connected to {c_ip}")
				res = ""
				try:
					res = self.recieve(client)
					print(res)
					handler_result = self._server_backend.client_handler(res)

					if handler_result != None:
						command, command_id, count = handler_result
						print(f"command: {command}, command_id: {command_id}, count: {count}")
						#not_ready, command, sudo, password, sequence, depot_items, command_id=0
						self._server_msg.add_data(False, command, "", "", 0, count, command_id)
						self.send(client)
					else:
						print("None")
						# create a situation where it can return a message for the client to wait for the server
						# and the server can ping the client to wake it up
					# self.client_handler(res)

					# self._server_msg.add_data(command, sudo, password, sequence, depot_items, )
					# self._server_msg.add_data("ls -al", False, "", 0, 3)

				except:
					pass
				client.close()
		except KeyboardInterrupt:
			print("\n Keyboard Interupt")
			self._server.close()
			if client != None:
				print("client closed")
				client.close()

if __name__ == "__main__":
	s = Server("localhost", 9999, 5)
	s.server_loop()
