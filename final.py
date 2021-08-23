import numpy as np
import pandas as pd
import pickle
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import string
import requests

# finalises the data into its own csv
file_read = open('teams.csv', 'r')
file_final = open('final.csv', 'w', newline='')
writer = csv.writer(file_final)
for row in csv.reader(file_read):
    if any(field.strip() for field in row):
        writer.writerow(row)
file_read.close()
file_final.close()