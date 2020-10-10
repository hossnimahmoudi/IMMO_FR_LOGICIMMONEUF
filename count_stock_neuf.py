import csv
import sys

csv_name = sys.argv[1]



STOCK_NEUF = 0
stock_neuf_index = None

with open(csv_name) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=';')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			stock_neuf_index = row.index("STOCK_NEUF")
			line_count += 1
		else:
			try : 
				c = float(row[stock_neuf_index])
				STOCK_NEUF += c 
			except : 
				pass 
print "STOCK_NEUF = " , STOCK_NEUF
