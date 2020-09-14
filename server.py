from shared import tcp_socket_handler

from backseat_server import client_handler

socket_handler = tcp_socket_handler.TcpSocketHandler()

server = socket_handler.create_server("localhost", 9999, 5)
client = None
try:
	while True:
		client, src_ip = server.accept()
		ip, port = src_ip
		#recieve from endpoint
		res, sender_key = socket_handler.recieve(client, "private.pem")
		print(f"Sender - {sender_key}:\n{res}")
		#convert string to python dict
		#send it through client_handler


		#send responce
		socket_handler.send(client, "---Recieved---", "public.pem", "private.pem")

except KeyboardInterrupt:
	print("\n--Keyboard Interrupt--")
	server.close()
	if client != None:
		client.close()


# s.server_loop()
