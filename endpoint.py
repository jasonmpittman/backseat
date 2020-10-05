# from shared import tcp_socket_handler

# socket_handler = tcp_socket_handler.TcpSocketHandler()

# client_socket = socket_handler.create_client_socket_connect("localhost", 9999)

from backseat_endpoint import endpoint

E = endpoint.Endpoint("localhost", 9999, "private.pem", "public.pem")
E.operate()
