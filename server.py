from shared import tcp_socket_handler

from backseat_server import client_handler

import json

from backseat_server import server_message

from pprint import pprint
socket_handler = tcp_socket_handler.TcpSocketHandler()

cli_handler = client_handler.ClientHandler()

server_msg = server_message.ServerMessage()

server = socket_handler.create_server("localhost", 9999, 5)
client = None

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

except KeyboardInterrupt:
	print("\n--Keyboard Interrupt--")
	server.close()
	if client != None:
		client.close()


# s.server_loop()
