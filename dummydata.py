#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 00:43:49 2019

@author: manzars
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver

url = "https://www.in.pampers.com/pregnancy/baby-names/article/top-indian-baby-names"
req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')
table = soup.findAll('table')
male = []
female = []
female_td = table[0].findAll('td')[::2]
male_td = table[1].findAll('td')[::2]
for td in male_td:
        male.append(td.text)

for td in female_td:
        female.append(td.text)

surname_url = "https://www.momjunction.com/articles/popular-indian-last-names-for-your-baby_00334734/#gref"
req = requests.get(surname_url)
soup = BeautifulSoup(req.text, 'lxml')
h3 = soup.findAll('h3')
surnames = []
for surname in h3[:-8]:
    surnames.append(surname.text.split(' ')[1].replace(':', ''))

disease_url = "https://www.nhp.gov.in/disease-a-z/"
alphabet = []
for alp in range(97, 123):
    alphabet.append(chr(alp))

wb = webdriver.Chrome("/home/manzars/Downloads/chromedriver")
disease_url = "https://www.nhp.gov.in/disease-a-z/"
disease = []
for i in alphabet:
    link = disease_url + i
    wb.get(link)
    html = wb.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    div = soup.findAll('div', {'class': 'all-disease'})
    lis = div[0].findAll('li')
    for li in lis:
        disease.append(li.text.rstrip())
wb.close()

with open("maleName.txt", 'w') as f:
    for s in male:
        f.write(str(s) + '\n')
with open("femaleName.txt", 'w') as f:
    for s in female:
        f.write(str(s) + '\n')
with open("surname.txt", 'w') as f:
    for s in surnames:
        f.write(str(s) + '\n')
with open("disease.txt", 'w') as f:
    for s in disease:
        f.write(str(s) + '\n')
