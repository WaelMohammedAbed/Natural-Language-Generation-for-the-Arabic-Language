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


mycursor.execute("SELECT * FROM `adjectives_root`")

adjectives_roots = mycursor.fetchall()

for adjectives_root in adjectives_roots:

    url='https://en.wiktionary.org/wiki/'+adjectives_root['adjective_root']
    try:
        # Connect to the URL
        response = requests.get(url)
        response.encoding = "utf-8"
        soup =BeautifulSoup(response.text, "html.parser")
        for div in soup.find_all('div', attrs={'class':'NavFrame'}):
            div_head=div.find('div',attrs={'class':'NavHead'});
            if "Declension of adjective" in div_head.text.strip():
                div_content=div.find('div',attrs={'class':'NavContent'})
                inflection_table=div_content.find('table',attrs={'class':'inflection-table'})
                with codecs.open("adjectives_tables/arabic_adj_"+str(adjectives_root['id'])+".html", "a", encoding="utf-8") as f2:
                    f2.write(str(inflection_table))
                break
    except:
        continue
