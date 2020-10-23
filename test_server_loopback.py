from shared import tcp_socket_handler


import json


SH = tcp_socket_handler.TcpSocketHandler("server_private.pem", "server_public.pem")


client = SH.create_client_socket_connect("localhost", 9999)


# message_dict = {"type": "add", "command": "PWD", "who": ["client1_public.pem"]}
message_dict = {"type": "checkoff", "command_id": 3, "who": "client1_public.pem"}
message = json.dumps(message_dict)
SH.send(client, message, "server_public.pem")


'''
command
who
'''

"""
type: checkoff
command_id
depot
"""
