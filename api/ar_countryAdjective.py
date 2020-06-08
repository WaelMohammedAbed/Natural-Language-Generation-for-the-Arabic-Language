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

mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])




def get_country_adjective(country,
                        number_form = "singular",
                        case="nominative",
                        gender=True,
                        is_human=True,
                        agreement=True):
    column="f_"
    if gender:
        column="m_"
    column=column+number_form+"_"+case

    select_country=("SELECT * FROM `country_adjective` WHERE "
                      +"`country` = %(country)s OR "
                      +"`m_singular_nominative` = %(country)s OR "
                      +"`m_singular_accusative` = %(country)s OR "
                      +"`m_singular_genitive`  = %(country)s OR "
                      +"`m_dual_nominative` = %(country)s OR "
                      +"`m_dual_accusative` = %(country)s OR "
                      +"`m_dual_genitive`  = %(country)s OR "
                      +"`m_plural_nominative` = %(country)s OR "
                      +"`m_plural_accusative`  = %(country)s OR "
                      +"`m_plural_genitive`  = %(country)s OR "
                      +"`f_singular_nominative` = %(country)s OR "
                      +"`f_singular_accusative` = %(country)s OR "
                      +"`f_singular_genitive`  = %(country)s OR "
                      +"`f_dual_nominative` = %(country)s OR "
                      +"`f_dual_accusative`  = %(country)s OR "
                      +"`f_dual_genitive` = %(country)s OR "
                      +"`f_plural_nominative` = %(country)s OR "
                      +"`f_plural_accusative` = %(country)s OR "
                      +"`f_plural_genitive` = %(country)s ORDER BY `country` = %(country)s DESC LIMIT 1")
    data_country = {
        'country': country,
    }
    cur = mysql.cursor(buffered=True,dictionary=True)

    cur.execute(select_country,data_country)
    countryDetails = cur.fetchone()

    country_adjective=""
    #check if the value in the database
    if(countryDetails == None or (countryDetails != None and countryDetails[column] == None)):
        #the value not in the database, therefore, get it manually
        return ""
    #else if it is in the database, then take it
    else:
        country_adjective=countryDetails[column]

    return country_adjective



def ar_countryAdjective(country,number= "singular", case="nominative", gender = True, is_human = True, agreement = True):
    country=str(country).strip()
    if(len(country)==0):
        return { 'error':True,'message':' country is mandatory and can\'t be empty'}


    is_arabic,word,message=is_arabic_word(country)
    if not is_arabic:
        return { 'error':True,'message':' error in country value: '+message}
    country=word
    #check if given case is a string and in one of these values ((nominative, accusative, genitive)
    if(case is None or len(str(case).strip())==0):
        case="nominative"
    else:
        if (isinstance(case,str) and case.strip().lower() in ["nominative","accusative","genitive"]):
            case=case.strip().lower()
        else:
            return False,"case value is not valid"

    #check if given gender is in string or int format and in one of these values (0,1,"m","f","male" or "female")
    try:
        gender = int(gender)
    except :
        gender=str(gender)
    if(gender is None or len(str(gender).strip())==0):
        gender=True
    else:
        if (isinstance(gender,str) and gender.strip().lower() in ["male","m"]):
            gender=True
        if (isinstance(gender,str) and gender.strip().lower() in ["female","f"]):
            gender=False
        elif (isinstance(gender,int) and int(gender) in [0,1]) or isinstance(gender,bool):
            if(gender):
                gender=True
            else:
                gender=False
        else:
            return { 'error':True, 'message':' gender value is not valid'}



    try:
        number = int(number)
    except :
        number=str(number)
    if(number is None or len(str(number).strip())==0):
        number="singular"
    else:
        if isinstance(number,str) and (str(number).strip().lower() in ["singular","dual","plural"]):
            number=str(number).strip().lower()
        elif isinstance(number,int):

            if number<0:
                number = number * -1
            if(number==1 or number == 0):
                number="singular"
            elif(number==2):
                number="dual"
            else:
                number="plural"
        else:
            return { 'error':True,'message':'number value is not valid'}

    inflected_country_adjective=get_country_adjective(country,number,case,gender,is_human,agreement)
    if len(inflected_country_adjective)>0:
        return { 'result':inflected_country_adjective, 'error':False, 'message':""}
    else:
        return { 'error':True,'message':'No result found'}
