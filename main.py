import numpy as np
import scipy as sp
import scipy.optimize as op
import urllib
import itertools


def calc_cum_returns(prices):
	return map(lambda x : x / prices[0], prices)

def get_prices(symbol):
	try:
		if price_lookup.has_key(symbol):
			return price_lookup[symbol]
		
		url = "http://ichart.finance.yahoo.com/table.csv?s={0}&a=00&b=1&c=2011&d=11&e=31&f=2011&g=d&ignore=.csv".format(symbol)
		days = urllib.urlopen(url).readlines()
		days.reverse();
		days.pop();
		prices = map(lambda x: float(x.split(",")[6]), days)		
		price_lookup[symbol] = prices;
		returns = calc_cum_returns(prices)
		return returns
	except Exception as e:
		print e
		return list()

def calc_port_daily_amounts(weights):
	global arbitrary_initial_amount
	port_prices = list()
	for dayIndex in xrange(len(data[0])):
		value = 0
		for weightIndex in xrange(len(weights)):
			current_balance = arbitrary_initial_amount * weights[weightIndex] * data[weightIndex][dayIndex]
			value = value +  current_balance
		port_prices.append(value)
	return port_prices


		
def calc_daily_returns(prices):
	returns = list()
	for index in xrange(1, len(prices)):
		returns.append(prices[index]/prices[index-1]-1)
	return returns;
		

def calc_sharpe_ratio(weights):
	global k
	weight_prices = calc_port_daily_amounts(weights)
	daily_returns = calc_daily_returns(weight_prices)
	std_dev = np.std(daily_returns)
	avg_return = np.average(daily_returns)
	value = k * avg_return / std_dev
	return value;

def grade_sharpe_ratio(weights):
	global k
	global arbitrary_initial_amount
	weight_prices = calc_port_daily_amounts(weights)
	print "port daily amounts: {0}".format(weight_prices)
	daily_returns = calc_daily_returns(weight_prices)
	print "port daily returns: {0}".format(daily_returns)
	std_dev = np.std(daily_returns)
	print "std. deviation: {0}".format(std_dev)
	avg_return = np.average(daily_returns)
	print "avg. return: {0}".format(avg_return)
	value = k * avg_return / std_dev
	print "sharpe ratio: {0}".format(value)
	print "annual return: {0}".format((weight_prices[-1]/arbitrary_initial_amount)-1)
	return value;

def sharpe_optimize(weights):
	return -calc_sharpe_ratio(weights)

def compare_result(x, y):
	if x[0] <= y[0]:
		return y
	return x

def setup_data(symbols):
	global data
	data = []
	for symbol in symbols:
		prices = get_prices(symbol)
		data.append(prices)

def test(symbols):
	setup_data(symbols)
	guess = sp.ones(len(symbols), dtype=float) * (1.0/len(symbols))
	cons = ({'type':'eq', 'fun': lambda x: np.sum(x) - 1})
	bounds = map(lambda x : (0.0, 1.0), symbols)
	optimization = op.minimize(sharpe_optimize, guess, method="SLSQP", bounds=bounds, constraints=cons)
	result = [optimization['fun'] * -1, zip(symbols, map(lambda m : 0 if m < 1E-5 else m, optimization['x']))]
	global best
	best = compare_result(result, best)
	if (best[0] == result[0]):
		print "best so far: {0}".format(best)
		results.append(best)

def grade(symbols, weights):
	setup_data(symbols)
	grade_sharpe_ratio(weights)
	
	

arbitrary_initial_amount = 1000000
price_lookup = dict()		
data = []
results = []
best = [-50, ["whatever"]]
k = 252**.5



file = open("atleast20.txt")
companies = []
while 1:
	line = file.readline()
	if not line:
		break
	companies.append(line.strip())
file.close()



print "# of comps: {0}".format(len(companies))
fail_count = 0
count = 0

sets = itertools.combinations(companies, 4)
for s in sets:
	symbols = list(s)
	test(symbols)
	if (count%1000==0):
		print count
	count = count+1


print "the best: {0}".format(best)	
	
	

