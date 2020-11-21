from shared import tcp_socket_handler

TCP = tcp_socket_handler.TcpSocketHandler("server_private.pem", "server_public.pem")
client = TCP.create_client_socket_connect("localhost", 9998)

TCP.send(client, "_", "client1_public.pem")

# FORCE RUN WORKS!!!
