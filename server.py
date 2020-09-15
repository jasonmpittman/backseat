from shared import tcp_socket_handler

from backseat_server import client_handler

import json

socket_handler = tcp_socket_handler.TcpSocketHandler()

cli_handler = client_handler.ClientHandler()

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
		cli_handler.client_handler(res_dict, sender_key)


		#send responce
		socket_handler.send(client, "---Recieved---", "public.pem", "private.pem")

except KeyboardInterrupt:
	print("\n--Keyboard Interrupt--")
	server.close()
	if client != None:
		client.close()


# s.server_loop()
