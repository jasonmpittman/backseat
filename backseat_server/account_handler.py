'''
Handles the user accounts that need to access the server through the UI.

'''

import hashlib

from shared import log_handler

class AccountHandler:
	"""
	Handles the user accounts associated with those who will use the server
	UI.

	Attributes
	----------
	_accounts : list
	"""
	def __init__(self):
		"""
		This function sets up the _accounts list by getting the information
		from the accounts.config file.

		Parameters
		----------
		"""
		self._log = log_handler.LogHandler(self.__class__.__name__)
		try:
			f = open("accounts.config")
			file_lines = f.readlines()
			f.close()
			self._accounts = []
			for file_line in file_lines:
				file_line = file_line.strip("\n")
				usr, pword = file_line.split(",")
				self._accounts.append({"username": usr, "password": pword})
			self._log.info("__init__", "Accounts loaded from accounts.config")
		except Exception as E:
			self._log.error("__init__", "Accounts could not be loaded from accounts.config - returned None")
			print(E)
			return None


	def _hash(self, str_obj):
		"""
		This function returns a sha512 hash of what ever string is passed in.

		Parameters
		----------
		str_obj : str
		"""
		try:
			return hashlib.sha512(f"{str_obj}".encode()).hexdigest()
		except Exception as E:
			self._log.error("_hash", "Hashing failed - returned None")
			print(E)
			return None

	def verify(self, username, password):
		"""
		This checks if a given username password pair has an account. It hashes
		the password and checks it against the stored hashed password.

		Parameters
		----------
		username : str
		password : str
		"""
		for account in self._accounts:
			if account["username"] == username:
				if self._hash(password) == account["password"]:
					self._log.info("verify", "Username and password correct - Returned True")
					return True
				else:
					self._log.info("verify", "Password or username incorrect - Returned False")
					return False
		self._log.warning("verify", "Password or username incorrect - Returned False")
		return False

	def add_account(self, username, password):
		"""
		Adds an account to the accounts.config file after checking to ensure
		no duplicate usernames.

		Parameters
		----------
		username : str
		password : str
		"""
		for a in self._accounts:
			if a["username"] == username:
				self._log.error("add_account","Username already in use - Returned None")
				return None
		account = {"username": username, "password": self._hash(password)}
		self._accounts.append(account)
		file = open("accounts.config", "w")
		for acc in self._accounts:
			file.write(f"{acc['username']},{acc['password']}\n")

		file.close()
		self._log.info("add_account", "Account information has been written to accounts.config")


if __name__ == "__main__":
	AH = AccountHandler()
