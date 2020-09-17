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
		print(f"Sender - {sender_key}:\n{res}")
		#convert string to python dict
		# print("@@@@@@@@@@@@@@@@@@@@@@@@")
		# print(res)
		# print("@@@@@@@@@@@@@@@@@@@@@@@@\n")
		# new_string =""
		# for letter in res:
		# 	new_string += letter

		res_dict = json.loads(res)
		print(f"res_dict: {type(res_dict)}")
		print(res_dict["ping"])

		# print(res_dict["ping"])
		# raw_str = r""
		# print("AAAAAAAA")
		# read_text = False
		# key = True
		# word = ""
		# parts = []
		# for q in res_dict:
		# 	# if q == '"' and read_text == False:
		# 	# 	read_text = True
		# 	# if q == '"' and read_text == True:
		# 	# 	read_text = False
		# 	print(f"{q}: {read_text}")
		# 	if q == '"':
		# 		if read_text == True:
		# 			read_text = False
		# 			parts.append(word)
		# 			word = ""
		# 		else:
		# 			read_text = True
		# 	else:
		# 		word += q
		# print(parts)



		print(raw_str)
		print("AAAAAAAA")
		print("###")

		print(type(res_dict))
		print("###")
		print("--")
		# print(type(res_dict[0]))
		#send it through client_handler
		next_depot_item = cli_handler.client_handler(res_dict, sender_key)
		#command
		#command_id
		# not_ready, command, sudo, password, sequence, depot_item, command_id
		print(next_depot_item)
		responce_msg_json = server_msg.create_msg(False, next_depot_item["command"], False, "", 0, next_depot_item["depot_count"], next_depot_item["command_id"])


		#send responce
		socket_handler.send(client, responce_msg_json, "public.pem", "private.pem")

except KeyboardInterrupt:
	print("\n--Keyboard Interrupt--")
	server.close()
	if client != None:
		client.close()


# s.server_loop()
