#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 16:38:19 2019

@author: macbook
"""

import scholarly
import re 
from lxml import html
import webbrowser
import urllib.request
from bs4 import BeautifulSoup as bs

search_term = input("Search Terms: ")
limit = input ("Number of articles to parse: ")


search_query = scholarly.search_pubs_query(search_term)
print(type(search_query))
successes = []

def main(text):
    ids = []
    text = re.sub('[^A-Za-z0-9\s]+',' ',text)
    textArr = text.split(" ")
    for s in textArr:
        if len(s) == 4:
            if any(char.isdigit() for char in s) and any(char.isalpha() for char in s) and s not in ids :
                ids.append(s)
                #print(s)
                pdb_url(s)

def pdb_url (pdb):
    
    url = 'https://www.rcsb.org/structure/' + pdb
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    soup = bs(respData, 'lxml')  
    if "Bad Request" not in soup.find('h1'):
        print (url)
        successes.append(url)
    #webbrowser.get('safari').open_new_tab(url)
    return url

i = 0
urls = []
for entry in search_query: 
    try:
        entry = str(entry)
        url = re.search("url': '(.*)'},", entry)
        url = url.group(1)
        #print(url)
        urls.append(url)
        
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        soup = bs(respData, 'lxml')  
        paragraphs = soup.findAll('p')
        for p in paragraphs: 
            p = p.text
            main(p)
        #main(str))
        
     
        
    except:
        pass
    i += 1
    if i > limit:
        break
        

#print(str(next(search_query)))
