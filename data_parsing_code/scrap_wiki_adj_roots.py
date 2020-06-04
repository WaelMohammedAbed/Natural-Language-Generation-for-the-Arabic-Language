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



def insertAdjectiveRoot(adjective):
    insert_query=("INSERT INTO `adjectives_root`( `adjective_root`) VALUES (%(adjective)s)")
    insert_data = {
      'adjective': adjective,
    }
    mycursor.execute(insert_query,insert_data)
    mysql.commit()
    return


frist_adj="آت"
for i in range(10):#range(44):
    url='https://en.wiktionary.org/w/index.php?title=Category:Arabic_adjectives&pagefrom='+frist_adj

    # Connect to the URL
    response = requests.get(url)
    response.encoding = "utf-8"
    adjectives=[]

     # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html.parser")
    div= soup.find('div', attrs={'id':'mw-pages'})


    try:
        for ul in div.findAll('ul'):
            for li in ul.findAll('li'):
                a=li.find('a')
                adjectives.append(a.text.strip())
                frist_adj=a.text.strip()
                insertAdjectiveRoot(frist_adj)

    except Exception as e:
        continue

    print(frist_adj)
