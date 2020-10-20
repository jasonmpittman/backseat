from shared import tcp_socket_handler

SH = tcp_socket_handler.TcpSocketHandler("server_private.pem", "server_public.pem")

client = SH.create_client_socket_connect("localhost", 9999)

SH.send(client, message, "server_public.pem")
