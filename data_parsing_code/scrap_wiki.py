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
    url='https://en.wiktionary.org/wiki/'+verb_root['verb_root']

    # Connect to the URL
    response = requests.get(url)
    response.encoding = "utf-8"
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        div= soup.find('div', attrs={'class':'NavFrame ar-conj'})
        div_content=div.find('div',attrs={'class':'NavContent'})
        inflection_table=div_content.find('table',attrs={'class':'inflection-table'})
        with codecs.open("verbs_tables/arabic_verb_"+str(verb_root['id'])+".html", "a", encoding="utf-8") as f2:
            f2.write(str(inflection_table))
    except:
        continue
