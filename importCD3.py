#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:59:32 2017

@author: jem
"""
import os.path
from os.path import basename
import psycopg2
import sqlite3
import statistics
import zipfile

import lmoments
import yaml
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import os

import csv
root = Tk()
root.withdraw()
root.update()
pathtoopen = filedialog.askopenfilename(initialdir="", title="choose CD3 file",
                                           filetypes=(("CD3 files", "*.CD3"), ("all files", "*.*")))
with open(pathtoopen) as f:
    d = dict(filter(None, csv.reader(f)))

print(d)
