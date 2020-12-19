import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def loadStockHistoricals(symbol):
	
	rawHistoricals = readJSON(stockJSONFilename(symbol))
	return processStockHistoricals(rawHistoricals)

def loadOptionHistoricals(symbol):

	return readJSON(optionJSONFilename(symbol))

def stockJSONFilename(symbol):
	return "/stocks/stockJSON/{}.json".format(symbol.upper())

def optionJSONFilename(symbol):
	return "options/optionJSON/{}.json".format(symbol.upper())

def readJSON(filename):

	data_file = open(filename, "r")
	data = json.load(data_file)
	data_file.close()

	return data

def processStockHistoricals(rawHistoricals):

	for time in list(data.keys()):
			for attribute in list(data[time].keys()):
				if type(data[time][attribute]) == str:
					data[time][attribute] = eval(data[time][attribute])
	return data