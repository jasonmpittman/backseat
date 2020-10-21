# from shared import tcp_socket_handler

# socket_handler = tcp_socket_handler.TcpSocketHandler()

# client_socket = socket_handler.create_client_socket_connect("localhost", 9999)
import sys
from backseat_endpoint import endpoint_operation
from shared import read_server_config

#serv_ip, serv_port, my_private_key, my_public_key, server_public_key

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print(f"Needs 2 command line arguement [my_private_key, my_public_key ], {len(sys.argv)-1} provided")
		exit()

	ip, port, server_public_key = read_server_config.get_server_config()
	my_private_key = sys.argv[1]
	my_public_key = sys.argv[2]

	E = endpoint_operation.EndpointOperation(ip, port, my_private_key, my_public_key, server_public_key)
	# E.operate()
	E.operation_loop()
