# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
#reads csv in and puts in it in alist of tuples
with open('/Users/jem/WINFAP-FEH_v4.1/gore water.csv', 'r') as f:
  reader = csv.reader(f)
  your_list = list(reader)

#gets first element in each tuple
#res_list = [x[0] for x in your_list]
#print(res_list)
print(your_list)

bob = ','.join(your_list[2][2:4])

print(bob)