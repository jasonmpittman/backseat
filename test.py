from backseat_server import registration_handler

from backseat_server import command_handler

from shared import asym_cryptography_handler

from backseat_server import account_handler

AH = account_handler.AccountHandler()

print(AH.hash("password"))
