from backseat_server import server_update_handler

SUH = server_update_handler.ServerUpdateHandler()




SUH.add_command("ls", ["client1_private.pem"])

info = SUH.get_info_message()
print("Test", info)
print(type(info))
print(info["depots_state"])
