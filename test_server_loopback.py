from backseat_server import server_update_handler
import time
SUH = server_update_handler.ServerUpdateHandler()




# SUH.add_command("ls", ["client1_public.pem"])

info = SUH.get_info_message()
print(info["depots_state"])
print("---------")
# SUH.override_command(2, "client1_public.pem")

info = SUH.get_info_message()
SUH.print_info_message(info)
# print(time.strftime("%a, %b %d, %Y %I:%M:%S %p", time.localtime(info["start_time"])))
