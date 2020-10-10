import csv
from csv import QUOTE_ALL
from datetime import date
import re
import sys
csv_name = sys.argv[1]
new_csv_name = sys.argv[2]
key_dup = sys.argv[3]
i = 0 
index = 0 
with open(csv_name, newline='') as csvfile , open(new_csv_name, "w" ,  newline='') as f :
	f2 = csv.writer(f, delimiter=';', quotechar='"',quoting=QUOTE_ALL)
	spamreader = csv.reader(csvfile, delimiter=';') 
	#quotechar='')
	dict_set = {}
	head = ""
	for row in spamreader : 
		if  i == 0 : 
			print( row.index(key_dup))
			head = row
		else : 
			dict_set[row[head.index(key_dup.strip())].strip()] = row
		i += 1 
	f2.writerow(head)
	for itm in dict_set.keys() : 
		f2.writerow(dict_set[itm])
print("the new csv containe {0} line , it was remouved the duplicated bassing on field {1} , >>>>>>>>> {2} was duplicated ".format(len(dict_set.keys()),key_dup,i - len(dict_set.keys())))
