import socket

from shared import asym_cryptography_handler as crypto

import os

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
				cyphertext = self._crypto.encrypt(block, public_key)
				cyphertext_full_msg += cyphertext
		except:
			print("TcpSocketHandler.send(): error in encrypting blocks")
			return None
		try:
			signature = self._crypto.sign(cyphertext_full_msg, private_key)
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


	def recieve(self, client, private_key):
		signed_msg = b''
		return_msg = r""
		try:
			while True:
				raw_msg = client.recv(1024)
				if not raw_msg:
					break
				signed_msg += raw_msg
		except:
			print("TcpSocketHandler.recieve(): Error in recieving message")
			return None
		client_msg = signed_msg[:-256]
		client_signature = signed_msg[-256:]
		sender_public_key = self._identify(client_msg, client_signature)
		print("sender public key: ", sender_public_key)
		msg_byte_blocks = self._byte_splitter(client_msg)

		try:
			for block in msg_byte_blocks:
				return_msg += self._crypto.decrypt(block, private_key)
				print("--return_msg--")
				print(return_msg)
		except:
			print("TcpSocketHandler.recieve(): Error in decryption of the message")
			return None
		# print("return message:")
		# print(return_msg)

		# print("##---##")
		# return_msg = self._clean_up(return_msg)
		# print(return_msg)
		return return_msg, sender_public_key


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

	def _get_key_list(self):
		arr = os.listdir("keys")
		return arr

	def _identify(self, obj, signature):
		key_list = self._get_key_list()
		print(f"key_list: {key_list}")
		print(f"obj: {obj}")
		print(f"signature: {signature}")
		for key in key_list:
			if self._crypto.is_sign_valid(obj, signature, key) == True:
				return key
		return None

	def _clean_up(self, escape_string):
		out = escape_string.encode().decode('unicode_escape')
		return out
