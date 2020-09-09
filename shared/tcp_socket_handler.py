import socket

import asym_cryptography_handler as crypto

# AsymmetricCryptographyHandler()
# Note on the asym_crypto:
	# 245 character encrytion limit
	# 256 byte encryption output
	# 256 byte signature output



class TcpSocketHandler:
	Crypto_Character_Limit = 245
	Crypto_Byte_Output = 256
	def __init__(self):
		pass

	def send(self, client):
		pass

	def recieve(self, client):
		pass

	def create_client_socket_connect(self, ip, port):
		try:
			connected_socket = socket.socket()
			connected_socket.connect((ip, port))
			return connected_socket
		except:
			print(f"Failed to connect to (ip[{ip}], port[{port}])")
			return None

	def create_server(self, ip, port, total_connections):
		try:
			server = socket.socket()
			server.bind((ip, port))
			server.listen(total_connections)
			return server
		except:
			print(f"Failed to create, bind, or listen to (ip[{ip}], port[{port}])")
