from backseat_server import registration_handler

RH = registration_handler.RegistrationHandler()
RH.print_host_list()
print("--")
RH.delete_host("")
RH.print_host_list()
