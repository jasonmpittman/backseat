from shared import tcp_socket_handler

from backseat_server import client_handler

import json

from backseat_server import server_message

import threading

#comment below out
client = None

class ServerLoop():
	def __init__(self, ip, port, allowed_connections=10):
		self._socket_handler = tcp_socket_handler.TcpSocketHandler()
		self._cli_handler = client_handler.ClientHandler()
		self._server_msg = server_message.ServerMessage()
		self._server = self._socket_handler.create_server(ip, port, allowed_connections)
		self._client = None
		self._src_ip = None
		self._my_public_key = "public.pem"
		self._my_private_key = "private.pem"
		self._threads_list = []

	def server_iteration(self):
		theard_id = threading.get_ident()
		print(f"Thread ID = {theard_id}")
		res, sender_key = self._socket_handler.recieve(self._client, "private.pem")
		print(f"Sender - {sender_key}\n{res}")
		print("----")
		res_dict = json.loads(res)

		next_depot_item, count = self._cli_handler.client_handler(res_dict, sender_key)

		if next_depot_item != None:
			print(next_depot_item)

			responce_msg_json = self._server_msg.create_msg(False, next_depot_item["command"], False, "", 0, next_depot_item["depot_count"], next_depot_item["command_id"])
		else:
			responce_msg_json = self._server_msg.create_msg(True, "", False, "", 0, count, 0)

		self._socket_handler.send(self._client, responce_msg_json, sender_key, self._my_private_key)

	def server_loop(self):
		try:
			print("--Server Running--")
			while True:
				self._client, self._src_ip = self._server.accept()
				try:
					new_thread = threading.Thread(target=self.server_iteration())
					new_thread.start()
				except Exception as E:
					print("--Error in server_loop threading--")
					print(E)
					print("-- --")



		except KeyboardInterrupt:
			print("\n--Keyboard Interrupt--")
			self._server.close()
			if self._client != None:
				self._client.close()
