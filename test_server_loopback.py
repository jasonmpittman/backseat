from backseat_server import server_update_handler

SUH = server_update_handler.ServerUpdateHandler()


info = SUH.get_info_message()
print("Test", info)
print(type(info))
print(info["depots_state"])
