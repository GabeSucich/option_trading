
import json

def login():
	"""Go into credentials.json and add your robinhood login information."""

	data_file = open("../../credentials.json", "r")
	data = json.load(data_file)
	data_file.close()
	robin_stocks.login(data["username"], data["password"])
	print("Logged In")

login()