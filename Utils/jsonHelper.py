import os, sys

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root)

import json

def loadStockHistoricals(symbol):
	
	rawHistoricals = readJSON(stockJSONFilename(symbol))
	return processStockHistoricals(rawHistoricals)

def loadOptionHistoricals(symbol):

	return readJSON(optionJSONFilename(symbol))

def stockJSONFilename(symbol):
	return root + "/stocks/stockJSON/{}.json".format(symbol.upper())

def optionJSONFilename(symbol):
	return root + "/options/optionJSON/{}.json".format(symbol.upper())

def readJSON(filename):

	data_file = open(filename, "r")
	data = json.load(data_file)
	data_file.close()

	return data

def dumbJSON(data, filename):

	data_file = open(filename, "w")
	json.dump(data, data_file)
	data_file.close()

	return "{0} successfully updated".format(filename)

def processStockHistoricals(data):
	if "2020-11-27" in data:
		del data["2020-11-27"]
	for date in data:
		if "corrected" in data[date]:
			del data[date]["corrected"]
		for time in data[date]:
			for attribute in data[date][time]:
				if type(data[date][time][attribute]) == str:
					data[date][time][attribute] = eval(data[date][time][attribute])
	return data