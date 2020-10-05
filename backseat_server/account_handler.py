'''
Handles the user accounts that need to access the server through the UI.
- Hash password
- stored on computer
- Possible use pam

'''

import hashlib

class AccountHandler:
	def __init__(self):
		f = open("accounts.config")
		file_lines = f.readlines()

		f.close()
		self._accounts = []
		for file_line in file_lines:
			file_line = file_line.strip("\n")
			usr, pword = file_line.split(",")
			self._accounts.append({"username": usr, "password": pword})

		print(self._accounts)

	def _hash(self, str_obj):
		return hashlib.sha512(f"{str_obj}".encode()).hexdigest()


	def verify(self, username, password):
		for account in self._accounts:
			if account["username"] == username:
				if self._hash(password) == account["password"]:
					return True
				else:
					print("Password or username incorrect")
					return False
		print("Password or username incorrect")
		return False

	def add_account(self, username, password):
		for a in self._accounts:
			if a["username"] == username:
				print("Username already in use - Returned None")
				return None
		account = {"username": username, "password": self._hash(password)}
		self._accounts.append(account)
		file = open("accounts.config", "w")
		for acc in self._accounts:
			file.write(f"{acc['username']},{acc['password']}\n")
		file.close()


if __name__ == "__main__":

	AH = AccountHandler()
