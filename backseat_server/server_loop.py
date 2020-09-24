from shared import tcp_socket_handler

from backseat_server import client_handler

import json

from backseat_server import server_message

#comment below out
client = None

class ServerLoop:
	def __init__(self, ip, port, allowed_connections=10):
		self._socket_handler = tcp_socket_handler.TcpSocketHandler()
		self._cli_handler = client_handler.ClientHandler()
		self._server_msg = server_message.ServerMessage()
		self._server = self._socket_handler.create_server(ip, port, allowed_connections)
		self._client = None
		self._src_ip = None
		self._my_public_key = "public.pem"
		self._my_private_key = "private.pem"

	def server_loop(self):
		try:
			print("--Server Running--")
			while True:
				self._client, self._src_ip = self._server.accept()

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
		except KeyboardInterrupt:
			print("\n--Keyboard Interrupt--")
			self._server.close()
			if self._client != None:
				self._client.close()








'''
try:
	while True:
		client, src_ip = server.accept()
		ip, port = src_ip
		#recieve from endpoint
		res, sender_key = socket_handler.recieve(client, "private.pem")
		#if sender_key == None -- unrecognized user
		print(f"Sender - {sender_key}\n{res}")
		print("----")
		print(res)

		res_dict = json.loads(res)
		print(f"res_dict: {type(res_dict)}")
		print(res_dict["ping"])

		#send it through client_handler

		#stops client server from sending a responce to client if there is no depot item
		next_depot_item, count = cli_handler.client_handler(res_dict, sender_key)
		if next_depot_item != None:
			print(next_depot_item)
			responce_msg_json = server_msg.create_msg(False, next_depot_item["command"], False, "", 0, next_depot_item["depot_count"], next_depot_item["command_id"])
		#send responce
			socket_handler.send(client, responce_msg_json, "public.pem", "private.pem")
		else:
			responce_msg_json = server_msg.create_msg(True, "", False, "", 0, count, 0)
			socket_handler.send(client, responce_msg_json, "public.pem", "private.pem")
'''




# s.server_loop()
