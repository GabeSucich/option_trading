def wholeDayAveragePrice(historicals, date):

	relevant = historicals[date]
	total = 0
	count = 0
	for data in relevant.values():
		total += data["open_price"]
		total += data["close_price"]
		count += 2

	return round(total/count, 2)

def wholeDayHighPrice(historicals, date):

	relevant = historicals[date]
	return max([data["high_price"] for data in list(relevant.values())])

def wholeDayLowPrice(historicals, date):
	relevant = historicals[date]
	return min([data["low_price"] for data in list(relevant.values())])

def wholeDayOpenPrice(historicals, date):
	relevant = historicals[date]
	return list(relevant.values())[0]["open_price"]

def wholeDayClosePrice(historicals, date):
	relevant = historicals[date]
	return list(relevant.values())[-1]["close_price"]

def wholeDayVolume(historicals, date):
	relevant = historicals[date]
	return sum([data["volume"] for data in list(relevant.values())])

def intervalData(historicals, date, time):

	return historicals[date][time]

def intervalAveragePrice(historicals, date, time):

	relevant = intervalData(historicals, date, time)
	return round(relevant["open_price"]/2 + relevant["close_price"]/2 , 2)

def intervalHighPrice(historicals, date, time):

	return intervalData(historicals, date, time)["high_price"]

def intervalLowPrice(historicals, date, time):

	return intervalData(historicals, date, time)["low_price"]

def intervalOpenPrice(historicals, date, time):

	return intervalData(historicals, date, time)["open_price"]

def intervalClosePrice(historicals, date, time):

	return intervalData(historicals, date, time)["close_price"]

def intervalVolume(historicals, date, time):

	return intervalData(historicals, date, time)["volume"]






		





