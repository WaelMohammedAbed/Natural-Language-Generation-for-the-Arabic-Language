# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 22:47:34 2019

@author: Roaa
"""

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import mysql.connector as MySQL
mysql = MySQL.connect(host='localhost',
                      database='ar_nlg'
                      , user='root'
                      , password='')
mycursor = mysql.cursor(dictionary=True)


mycursor.execute("SELECT `id`,`verb_root` FROM `verbs` WHERE `id` > 72")

verb_roots = mycursor.fetchall()

for verb_root in verb_roots:
#for i in range(0,3):#[3120,3220,3320,3420,3520,3620,3720,3820,3920]:
    # Set the URL you want to webscrape from
    #url = 'https://cinemana.shabakaty.com/page/movie/watch/en/'+str(i)
    url='https://en.wiktionary.org/wiki/'+verb_root['verb_root']
    
    # Connect to the URL
    response = requests.get(url)
    response.encoding = "utf-8"
    try:
        # Parse HTML and save to BeautifulSoup object¶
        soup = BeautifulSoup(response.text, "html.parser")
        div= soup.find('div', attrs={'class':'NavFrame ar-conj'})
        div_content=div.find('div',attrs={'class':'NavContent'})
        inflection_table=div_content.find('table',attrs={'class':'inflection-table'})
        #comments_total_no=inflection_table.text
        with codecs.open("verbs_tables/arabic_verb_"+str(verb_root['id'])+".html", "a", encoding="utf-8") as f2:
            f2.write(str(inflection_table))
    #print(inflection_table)
    except:
        continue
    
    
