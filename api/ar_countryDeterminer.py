import mysql.connector as MySQL
from numeral_names import numeral_names
import yaml
import re

arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)

def remove_diacritics(text):
    try:
        text = re.sub(arabic_diacritics, '', text)
    except:
        return text

    return text

def is_arabic_word(word):
    word=str(word).strip()
    if len(re.findall(r'[\u0600-\u06FF]+', word)) <=0:
        return False,word,'the word is not Arabic, type not supported'
    else:
        try:
            word=remove_diacritics(word)
        except:
            return False,word,"the word could not remove the diacritics"
    return True,word,""





# Configure db
db = yaml.safe_load(open('db.yaml'))





def get_country_Determiner(country):
    column="country"
    country_with_the=country
    if country.startswith("ال"):
        country=country[2:]
    else:
        country_with_the="ال" + country_with_the

    select_country=("SELECT `country` FROM `country_adjective` WHERE "
                      +"`country` = %(country)s OR "
                      +"`country` = %(country_with_the)s  LIMIT 1")
    data_country = {
        'country': country,
        'country_with_the':country_with_the
    }
    mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])

    cur = mysql.cursor(buffered=True,dictionary=True)

    cur.execute(select_country,data_country)
    countryDetails = cur.fetchone()
    cur.close()
    mysql.close()

    country_determiner=""
    #check if the value in the database
    if(countryDetails == None or (countryDetails != None and countryDetails[column] == None)):
        #the value not in the database, therefore, get it manually
        return ""
    #else if it is in the database, then take it
    else:
        country_determiner=countryDetails[column]

    return country_determiner



def ar_countryDeterminer(country):
    country=str(country).strip()
    if(len(country)==0):
        return { 'error':True,'message':' country is mandatory and can\'t be empty'}

    is_arabic,word,message=is_arabic_word(country)
    if not is_arabic:
        return { 'error':True,'message':' error in country value: '+message}
    country=word

    country_Determiner=get_country_Determiner(country)
    if len(country_Determiner)>0:
        return { 'result':country_Determiner, 'error':False, 'message':""}
    else:
        return { 'error':True,'message':'No result found'}
