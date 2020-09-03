import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Utils.datetime_funcs import *
import json

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
	data = read_json("optionJSON/tracked_stocks.json")
	return list(data.keys())

def get_json_object(symbol):
	"""Returns the json object from the associated json file of name SYMBOL.json"""
	return read_json(json_filename(symbol))

def json_filename(symbol):
	"""Appends .json to the string SYMBOL"""
	return "stockJSON/" + symbol + ".json"