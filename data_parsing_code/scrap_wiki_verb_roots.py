
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



def insertVerbRoot(verb):
    insert_query=("INSERT INTO `verbs_root`( `verb_root`) VALUES (%(verb)s)")
    insert_data = {
      'verb': verb,
    }
    mycursor.execute(insert_query,insert_data)
    mysql.commit()
    return


first_verb="آتشيوت"
for i in range(44):#range(44):
    url='https://en.wiktionary.org/w/index.php?title=Category:Arabic_verbs&pagefrom='+first_verb
    
    # Connect to the URL
    response = requests.get(url)
    response.encoding = "utf-8"
    verbs=[]
    
     # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html.parser")
    div= soup.find('div', attrs={'id':'mw-pages'})
    

    try:
        for ul in div.findAll('ul'):
            for li in ul.findAll('li'):
                a=li.find('a')
                verbs.append(a.text.strip())
                first_verb=a.text.strip()
                insertVerbRoot(first_verb)

    except Exception as e:
        continue
        #print('Failed to scrap wiki: '+ str(e))

    print(first_verb)
    
    
