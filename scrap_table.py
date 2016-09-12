# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 22:51:50 2016

@author: PRAVEENKUMAR
"""


import csv
from bs4 import BeautifulSoup
from urllib2 import urlopen
soup = BeautifulSoup(urlopen('http://www.internetlivestats.com/internet-users-by-country/'))
table = soup.find('table', id = "example")
headers = [header.text for header in table.find_all('th')]
print headers
rows = []
for row in table.find_all('tr'):
    rows.append([val.text.encode('utf8') for val in row.find_all('td')])
#print row
with open('output_file.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(row for row in rows if row)
    
#cat output_file.csv