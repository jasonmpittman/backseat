from shared import tcp_socket_handler

from backseat_server import client_handler

import json

from backseat_server import server_message

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
		print(f"Sender - {sender_key}:\n{res}")
		#convert string to python dict
		res_dict = json.loads(res)
		#send it through client_handler
		next_depot_item, depot_item_count = cli_handler.client_handler(res_dict, sender_key)
		#command
		#command_id
		# not_ready, command, sudo, password, sequence, depot_item, command_id
		responce_msg_json = server_msg.create_msg(False, next_depot_item.command, False, "", 0, depot_item_count)


		#send responce
		socket_handler.send(client, "---Recieved---", "public.pem", "private.pem")

except KeyboardInterrupt:
	print("\n--Keyboard Interrupt--")
	server.close()
	if client != None:
		client.close()


# s.server_loop()
