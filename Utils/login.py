import robin_stocks
import json
import os

def login():
	"""Go into credentials.json and add your robinhood login information."""
	data_file = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/credentials.json", "r")
	data = json.load(data_file)
	data_file.close()
	robin_stocks.login(data["username"], data["password"], expiresIn = 120000)
	print("Logged In")

login()