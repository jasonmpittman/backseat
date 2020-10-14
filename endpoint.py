# from shared import tcp_socket_handler

# socket_handler = tcp_socket_handler.TcpSocketHandler()

# client_socket = socket_handler.create_client_socket_connect("localhost", 9999)
import sys
from backseat_endpoint import endpoint

#serv_ip, serv_port, my_private_key, my_public_key, server_public_key

if __name__ == "__main__":
	if len(sys.argv) != 6:
		print(f"Needs 5 command line arguements [server_ip, server_port, my_private_key, my_public_key server_public_key], {len(sys.argv)-1} provided")
		exit()
	ip = sys.argv[1]
	port = int(sys.argv[2])
	my_private_key = sys.argv[3]
	my_public_key = sys.argv[4]
	server_public_key = sys.argv[5]
	E = endpoint.Endpoint(ip, port, my_private_key, my_public_key, server_public_key)
	# E.operate()
	E.operation_loop()
