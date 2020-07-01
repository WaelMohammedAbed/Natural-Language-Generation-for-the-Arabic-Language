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



def insertNounRoot(noun):
    insert_query=("INSERT INTO `nouns_root`( `noun_root`) VALUES (%(noun)s)")
    insert_data = {
      'noun': noun,
    }
    mycursor.execute(insert_query,insert_data)
    mysql.commit()
    return


first_noun="آتشيوت"
for i in range(44):#range(44):
    url='https://en.wiktionary.org/w/index.php?title=Category:Arabic_nouns&pagefrom='+first_noun

    # Connect to the URL
    response = requests.get(url)
    response.encoding = "utf-8"
    nouns=[]

     # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html.parser")
    div= soup.find('div', attrs={'id':'mw-pages'})


    try:
        for ul in div.findAll('ul'):
            for li in ul.findAll('li'):
                a=li.find('a')
                nouns.append(a.text.strip())
                first_noun=a.text.strip()
                insertNounRoot(first_noun)

    except Exception as e:
        continue
        #print('Failed to scrap wiki: '+ str(e))

    print(first_noun)
