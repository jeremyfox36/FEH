#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:59:32 2017

@author: jem
"""

import csv
with open('/Users/jem/WINFAP-FEH_v4.1/Suitable for Pooling/3003.CD3') as f:
    d = dict(filter(None, csv.reader(f)))

print(d)
