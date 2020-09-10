import socket

import asym_cryptography_handler as crypto

# AsymmetricCryptographyHandler()
# Note on the asym_crypto:
	# 245 character encrytion limit
	# 256 byte encryption output
	# 256 byte signature output


class TcpSocketHandler:
	def __init__(self):
		self._crypto = crypto.AsymmetricCryptographyHandler()

	def send(self, client, message, public_key, private_key):
		blocks = self._create_message_blocks(message)
		cyphertext_full_msg = b''
		try:
			for block in blocks:
				cyphertext = self._crypto.encrypt(message, public_key)
				cyphertext_full_msg += cyphertext
		except:
			print("TcpSocketHandler.send(): error in encrypting blocks")
			return None
		try:
			signature = self._crypto.sign(cyphertext_full_msg, public_key)
			signed_msg = cyphertext_full_msg + signature
		except:
			print("TcpSocketHandler.send(): Error in signing message")
			return None
		try:
			client.send(signed_msg)
			client.shutdown(socket.SHUT_WR)
		except:
			print("TcpSocketHandler.send(): Error in sending message")
			return None


	def recieve(self, client, public_key, private_key):
		signed_msg = b''
		return_msg = ""

		while True:
			raw_msg = client.recv(1024)
			if not raw_msg:
				break
			signed_msg += raw_msg
		client_msg = signed_msg[:-256]
		client_signature = signed_msg[-256:]
		msg_byte_blocks = self._byte_splitter(client_msg)
		for block in msg_byte_blocks:
			return_msg += self._crypto.decrypt(block, private_key)
		return return_msg




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
			return None

	def _create_message_blocks(self, message):
		chunk_list = [message[i:i+245] for i in range(0, len(message), 245)]
		return chunk_list

	def _byte_splitter(self, message):
		chunk_list = [message[i:i+256] for i in range(0, len(message), 256)]
		return chunk_list
