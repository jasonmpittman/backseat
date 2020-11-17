# from shared import tcp_socket_handler

# socket_handler = tcp_socket_handler.TcpSocketHandler()

# client_socket = socket_handler.create_client_socket_connect("localhost", 9999)
import sys
from backseat_endpoint import endpoint_operation
from shared import read_server_config

#serv_ip, serv_port, my_private_key, my_public_key, server_public_key

def load_endpoint_config():
	f = open("endpoint.config", "r")
	data = f.read()
	list_data = data.split(" ")
	f.close()
	return list_data[0], list_data[1], list_data[2], list_data[3]


if __name__ == "__main__":

	my_ip, my_port, my_private_key, my_public_key = load_endpoint_config()

	ip, port, _, server_public_key = read_server_config.get_server_config()

	E = endpoint_operation.EndpointOperation(ip, port, my_ip, my_port, my_private_key, my_public_key, server_public_key)
	# E.operate()
	E.operation_loop()
