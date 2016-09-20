# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 22:51:50 2016

@author: PRAVEENKUMAR
"""


import csv
from bs4 import BeautifulSoup
from urllib2 import urlopen
import locale


def remove_percent(df,col):
    
    """
    remove percent symbol and convert the string to float
    """
    df[col] = df[col].str.strip()
    df[col] = df[col].map(lambda x: x.rstrip('%'))
    df[col] = df[col].astype(np.float)
    return df[col]
    
def remove_comma(df,col):
    
    """
    remove comma from a string
    """
    df[col] = df[col].str.strip()
    locale.setlocale(locale.LC_NUMERIC, '')
    df[col] = df[col].apply(locale.atoi)
    return df[col]
    
def scrap_table_to_csv(url,filename,id_table,is_class):

    soup = BeautifulSoup \
            (urlopen \
            (url))
    if is_class:
        table = soup.find('table', {"class" : id_table})
    else:
        table = soup.find('table', id = id_table)
    headers = [header.text for header in table.find_all('th')]
    print headers
    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text.encode('utf8') for val in row.find_all('td')])
    #print row
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)

def clean_internet_table(table):
    table['Penetration (% of Pop)'] = remove_percent(table,  \
                                  'Penetration (% of Pop)')
                                                      
    table['Users 1 Year  Change (%) '] = remove_percent(table, \
                                        'Users 1 Year  Change (%) ')  
    table['Population 1 Y Change']    = remove_percent(table,
                                'Population 1 Y Change')                                     
                                        
    table['Internet Users  (2016)']  =  remove_comma(table,    \
                                          'Internet Users  (2016)')                                 
    table['Internet Users 1 Year Change '] = remove_comma(table, \
                                            'Internet Users 1 Year Change ')                                                                             
    table['Population (2016)'] = remove_comma(table,'Population (2016)')
    table['Non-Users (internetless) '] = remove_comma(table, \
                                    'Non-Users (internetless) ')
    return table
import pandas
import numpy as np
scrap_table_to_csv \
    ('http://www.internetlivestats.com/internet-users-by-country/', \
    "output_file.csv","example",False)
    
table = pandas.read_csv("output_file.csv")

for val in table.columns:
    print ("Col Name is %s has data type %s"% (val,table[val].dtype))



print "After Conversion"

#Data Cleaning

table = clean_internet_table(table)

                           

#table= table.apply(pandas.to_numeric, args=('coerce',))
#for val in table.columns:
#    print ("Col Name is %s has data type %s"% (val,table[val].dtype))

print table['Population (2016)'].max()
print table['Users 1 Year  Change (%) '].max()

print "After Conversion"

for val in table.columns:
    print ("Col Name is %s has data type %s"% (val,table[val].dtype))

table.to_csv('data_cleaned.csv')
print "\nCSV File Created"
#
#scrap_table_to_csv \
#    ('http://www.internetlivestats.com/internet-users/india/', \
#    "india_file.csv","table",True)
table_india = pandas.read_csv("india_file.csv")
for val in table_india.columns:
    print ("Col Name is %s has data type %s"% (val,table_india[val].dtype))
print "After Conversion"
#table_india = clean_internet_table(internet_india)

table_india['Penetration (% of Pop) '] = remove_percent(table_india,  \
                                  'Penetration (% of Pop) ')
                                                      
table_india['1Y User  Change (%)'] = remove_percent(table_india, \
                                        '1Y User  Change (%)')  
table_india['Population  Change']    = remove_percent(table_india,
                                'Population  Change')                                     
                                        
table_india['Internet Users**']  =  remove_comma(table_india,    \
                                          'Internet Users**')                                 
table_india['1Y User Change '] = remove_comma(table_india, \
                                            '1Y User Change ')                                                                             

table_india['Non-Users (Internetless) '] = remove_comma(table_india, \
                                    'Non-Users (Internetless) ')
table_india['Total Population'] = remove_comma(table_india, \
                                    'Total Population')                                
print table_india['Year '].max()
for val in table_india.columns:
    print ("Col Name is %s has data type %s"% (val,table_india[val].dtype))
table_india.to_csv('india_data_cleaned.csv')
print "\nCSV File Created"
#scrap_table_to_csv \
#    ( 'http://statisticstimes.com/economy/countries-by-projected-gdp-capita-ppp.php', \
#    "gdp_file.csv","table_id",False)
gdp_world = pandas.read_csv("gdp_file.csv")
gdp_world['gdp_percapita'] = remove_comma(gdp_world, \
                                    '2015')
table['Continent'] = " "
table['gdp_percapita'] = " "
for val in table['Country']:
    if(any(gdp_world.Country == val)):
        Continent = gdp_world[gdp_world.Country == val].Continent
        table.loc[table.Country == val,'Continent'] = Continent.item()
        
        gdp = gdp_world[gdp_world.Country == val].gdp_percapita
        table.loc[table.Country == val,'gdp_percapita'] = gdp.item()
    else:
        print val
print table['Continent']     
table.to_csv('gdp_internet.csv')
#cat output_file.csv