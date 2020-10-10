#! /usr/bin/python3.5

import csv
from csv import QUOTE_ALL

f = open('LOGICIMMONEUF_06_2020_11_after_clean.csv', 'w')
with open('LOGICIMMONEUF_06_2020_11.csv') as csvfile:
    f2 = csv.writer(f, delimiter=';', quotechar='"',quoting=QUOTE_ALL)

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    for row in spamreader:

        f2.writerow(row)

