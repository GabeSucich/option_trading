
class Trader:

	def __init__(self, name, deposit):
		self.name = name
		self.stocks = []
		self.balance = deposit

	def add_funds(self, amount):
		self.balance += amount
		return "{0}, you have deposited {1} dollars into the account. Your current balance is {2}".format(self.name, amount, self.balance)

	def already_owns(self, stock_name):
		for stock in self.stocks:
			if stock.name == stock_name:
				return True
		return False

	def stock_index(self, stock_name):
		return self.stocks.index(stock_name)

	def buy_stock(stock_name, shares, price):
		if shares*price > balance:
			return "You don't have enough money to buy that stock. Stop trying to use your homies' money."
		elif self.already_owns(stock_name):
			self.stocks[stock_index(stock_name)].buy(shares, price)
			self.balance -= shares*price
			return "You have bought {0} more shares of {1}".formate(shares, stock_name)

			


		

class Stock:

	def __init__(self, name, shares, price):
		self.name = name
		self.average = price
		self.shares = shares

	def sell(self, shares, price):
		profit = shares*price - shares*self.average
		if shares > self.shares:
			return "You do not own {0} shares of {1}.".format(shares, self.name)
		else:
			self.shares -= shares
			if self.shares > 0:
				if profit >= 0:
					return "You made {0} dollars on your sale of {1}. You have {2} shares of {3} remaining.".format(profit, self.name, self.shares, self.name)
				else:
					return "You lost {0} dollars on your sale of {1}. You have {2} shares of {3} remaining.".format(abs(profit), self.name, self.shares, self.name)
			else:
				if profit >= 0:
					return "You made {0} dollars on your sale of all shares of {1}.".format(profit, self.name)
				else:
					return "You lost {0} dollars on your sale of all shares of {1}.".format(profit, self.name)

	def buy(self, shares, price):
		self.average = (self.shares*self.price + shares*price)/(shares + self.shares)
		self.shares += shares








