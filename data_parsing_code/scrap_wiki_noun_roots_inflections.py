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


mycursor.execute("SELECT * FROM `nouns_root`")

nouns_roots = mycursor.fetchall()

for nouns_root in nouns_roots:

    url='https://en.wiktionary.org/wiki/'+nouns_root['noun_root']
    try:
        # Connect to the URL
        response = requests.get(url)
        response.encoding = "utf-8"
        soup =BeautifulSoup(response.text, "html.parser")
        for div in soup.find_all('div', attrs={'class':'NavFrame'}):
            div_head=div.find('div',attrs={'class':'NavHead'});
            if "Declension of noun" in div_head.text.strip():
                div_content=div.find('div',attrs={'class':'NavContent'})
                inflection_table=div_content.find('table',attrs={'class':'inflection-table'})
                #comments_total_no=inflection_table.text
                with codecs.open("nouns_tables/arabic_noun_"+str(nouns_root['id'])+".html", "a", encoding="utf-8") as f2:
                    f2.write(str(inflection_table))
                break
    #print(inflection_table)
    except:
        continue




"""
url='https://en.wiktionary.org/wiki/'+"جميل"#nouns_root['noun_root']
    
# Connect to the URL
response = requests.get(url)
response.encoding = "utf-8"
soup =BeautifulSoup(response.text, "html.parser")
for div in soup.find_all('div', attrs={'class':'NavFrame'}):
    div_head=div.find('div',attrs={'class':'NavHead'});
    if "Declension of noun" in div_head.text.strip():
        div_content=div.find('div',attrs={'class':'NavContent'})
        inflection_table=div_content.find('table',attrs={'class':'inflection-table'})
        #comments_total_no=inflection_table.text
        with codecs.open("nouns_tables/aa1.html", "a", encoding="utf-8") as f2:
            f2.write(str(inflection_table))
        break
        
    
"""

    
    
