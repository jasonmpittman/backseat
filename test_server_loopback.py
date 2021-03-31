from backseat_server import server_update_handler
import time
SUH = server_update_handler.ServerUpdateHandler()


SUH.add_command("ls -al", False, "", ["client1_public.pem"])

info = SUH.get_info_message()
SUH.print_info_message(info)

