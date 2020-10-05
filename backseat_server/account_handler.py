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
		self.accounts = f.readlines()
		# Deal with the /n
		f.close()
		print(self.accounts)

	def hash(self, obj):
		return hashlib.sha512(f"{obj}".encode()).hexdigest()


if __name__ == "__main__":
	# text = "Te"
	# m = hashlib.sha256()
	# m.update(text.encode("utf-8"))
	# m.update("st".encode("utf-8"))
	# hashed = m.digest()
	# print(hashed)
	input = "Nobody inspects the spammish repetition"
	AH = AccountHandler()
	output = AH.hash(input)
	print(output)
	# print(type(ha))
