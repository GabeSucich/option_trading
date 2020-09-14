import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from stocks import *
from Utils.datetime_funcs import *
import json


def init_stock(symbol):

	instrument_data = get_instrument_data(symbol)
	if not instrument_data:
		print("{0} is not a valid symbol".format(symbol))
		return

	tracked_stocks_data = read_json("stockJSON/tracked_stocks.json")

	# if symbol in list(tracked_stocks_data.keys()):
	# 	print("Already tracking " + symbol)
	# 	return

	tracked_stocks_data[symbol] = instrument_data
	dump_json(tracked_stocks_data, "stockJSON/tracked_stocks.json")

	available_historical_data = get_all_recent_data(symbol)
	dump_json(available_historical_data, json_filename(symbol))


	print("{} initialized".format(symbol))

def update_stock_data(symbols = []):

	if not symbols:

		symbols = list_tracked_stocks()

	for symbol in symbols:

		print("Collecting stock data for " + symbol)
		json_data = read_json(json_filename(symbol))
		update_data_for_all_new_dates(symbol, json_data)
		dump_json(json_data, json_filename(symbol))
		print("Saving stock data for " + symbol)

def get_all_recent_data(symbol):

	historicals = get_stock_historicals(symbol)
	return format_raw_data(historicals)


def update_data_for_date(symbol, date, json_data, historicals):

	historicals_for_date = list(filter(lambda data_point : data_point["date"] == date, historicals))

	formatted_historicals = format_raw_data(historicals_for_date)
	json_data[date] = formatted_historicals[date]
	

def update_data_for_all_new_dates(symbol, json_data):

	new_dates = []

	historicals = get_stock_historicals(symbol)
	json_dates = list(json_data.keys())

	for data_point in historicals:

		if data_point["date"] not in json_dates:
			new_dates.append(data_point["date"])

	for date in new_dates:

		update_data_for_date(symbol, date, json_data, historicals)


def format_raw_data(raw_historicals):

	data = {}

	for data_point in raw_historicals:

		add_data_point(data_point, data)

	return data

"""Functions for converting raw data from Robinhood into storable JSON."""

def add_data_point(new_data_point, data):

	date = new_data_point["date"]
	time = new_data_point["time"]
	data_object = create_data_object(new_data_point)

	if date in list(data.keys()):

		if time not in list(data[date].keys()):

			data[date][time] = data_object

	else:

		data[date] = {}
		data[date][time] = data_object


def create_data_object(data_point):

	return {
		"open_price": str(data_point["open_price"]),
		"close_price": str(data_point["close_price"]),
		"high_price": str(data_point["high_price"]),
		"low_price": str(data_point["low_price"]),
		"volume": str(data_point["volume"])
		}		



"""Functions to read and write JSON into data files."""

def read_json(filename):
	"""FILENAME is the name of a json file containing option information. This function loads the json object into the script 
	to be edited. The return object is the option dictionary to be edited."""

	data_file = open(filename, "r")
	data = json.load(data_file)
	data_file.close()

	return data

def dump_json(updated_dict, filename):
	"""UPDATED_DICT is the option object with updated data. FILENAME is the name of the json file containing the option information.
	Run this function to update json files with new option data."""
	data_file = open(filename, "w")
	json.dump(updated_dict, data_file)
	data_file.close()

	return "{0} successfully updated".format(filename)

def list_tracked_stocks():
	"""Returns a list of all stock symbols for the stocks being tracker"""
	data = read_json("stockJSON/tracked_stocks.json")
	return list(data.keys())

def get_json_object(symbol):
	"""Returns the json object from the associated json file of name SYMBOL.json"""
	return read_json(json_filename(symbol))

def json_filename(symbol):
	"""Appends .json to the string SYMBOL"""
	return "stockJSON/" + symbol + ".json"






