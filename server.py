import socket

import server_message

import json

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
					# self.client_handler(res)

					# self._server_msg.add_data(command, sudo, password, sequence, depot_items, )
					self._server_msg.add_data("ls -al", False, "", 0, 3)

				except:
					pass
				client.close()
		except KeyboardInterrupt:
			print("\n Keyboard Interupt")
			if client != None:
				print("client closed")
				client.close()

if __name__ == "__main__":
	s = Server("localhost", 9999, 5)
	s.server_loop()
