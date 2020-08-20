'''
Handles everything involved with patches, gets them, and creates installation commands.

Interfaces with websites that have lists of security issues in software and OS's.
'''

import xmltodict

class PatchHandler:
	def __init__(self, depot_list=None):
		if depot_list == None:
			print("depot_list == None")
		self._depot_list = depot_list
		with open('backseat_server/allitems.xml') as fd:
			self._xml_doc = xmltodict.parse(fd.read())

if __name__ == "__main__":
	PH = PatchHandler()
	print("starting to print")
	# print(PH._xml_doc["cve"]["item"])
	listy = []
	for item in PH._xml_doc["cve"]["item"]:
		print("---")
		name = item["@name"]
		seq = item["@seq"]
		type = item["@type"]
		status = item["status"]
		try:
			phase = item["phase"]
		except:
			phase = "Failed"

		desc = item["desc"]
		try:
			refs = item["refs"]["ref"]
		except:
			print("candidate: " + str(item["refs"]))
			refs = None

		print("name: " + name)
		print("seq: " + seq)
		print("type: " + type)
		print("status: " + status)
		print("phase: " + str(phase))
		print("desc:" + desc)
		print("refs: ")
		print(refs)
		try:
			for ref in refs:
				print("\t" + ref["@source"])
				print("\t" + ref["@url"])
				print("\t" + ref["#text"])
				print("-")
		except:
			print("\tNone")

	print("finnishing printing")
