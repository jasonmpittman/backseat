from shared import tcp_socket_handler


socket_handler = tcp_socket_handler.TcpSocketHandler()

server = socket_handler.create_server("localhost", 9999, 5)
client = None
try:
	while True:
		client, src_ip = server.accept()
		ip, port = src_ip
		res = socket_handler.recieve(client, "public.pem", "private.pem")
		print(res)
except KeyboardInterrupt:
	print("\n--Keyboard Interrupt--")
	server.close()
	if client != None:
		client.close()


# s.server_loop()
