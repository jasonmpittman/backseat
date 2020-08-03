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

	def client_handler(self, client_json_str):
		client_dict = json.loads(client_json_str)
		if client_dict["completed"]:
			print("completed")
			if client_dict["successful"]:
				print("successful:")
				print(client_dict["stdout"])
			else:
				print("failed:\n")
				print(client_dict["stderr"])
		else:
			print("not completed")

		if client_dict["ready"]:
			print("Ready")

		print(f"id= {client_dict['command_id']}")
		print(f"exit_code= {client_dict['exit_code']}")

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
					res = client.recv(1024).decode()
					self.client_handler(res)

					# self._server_msg.add_data(command, sudo, password, sequence, depot_items)
					self._server_msg.add_data("ls -al", False, "", 0, 3)
					msg = self._server_msg.to_json()
					#encryption will occur at this point
					client.send(bytes(msg, Server.encoding))
					res = client.recv(1024).decode()
					print(json.loads(res)["stdout"])
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
