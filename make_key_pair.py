from shared import asym_cryptography_handler as crypto

import sys


if len(sys.argv) != 2:
	print(f"Needs 1 command line arguement [keypair name], {len(sys.argv)-1} provided")
	exit()
pair_name = sys.argv[1]

ACH = crypto.AsymmetricCryptographyHandler()
ACH.create_keys(pair_name)
