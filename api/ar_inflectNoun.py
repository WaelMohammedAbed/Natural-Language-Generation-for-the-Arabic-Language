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


def get_noun_dual_plural_gender(noun,case="nominative",gender = None,dual=None,plural=None,chosen_type="singular"):
    pluralByCase={'accusative': "plural_a", 'nominative': "plural_n", 'genitive':"plural_g"}
    dualByCase={'accusative': "dual_a", 'nominative': "dual_n", 'genitive':"dual_g"}
    singularByCase={'accusative': "singular_a", 'nominative': "singular_n", 'genitive':"singular_g"}

    select_singular=("SELECT * FROM `nouns` WHERE "
                     +"`singular_a` = %(noun)s "
                     +"OR `singular_n` = %(noun)s "
                     +"OR `singular_g` = %(noun)s "
                     +"OR `plural_a` = %(noun)s "
                     +"OR `plural_n` = %(noun)s "
                     +"OR `plural_g` = %(noun)s "
                     +"OR `dual_a` = %(noun)s "
                     +"OR `dual_n` = %(noun)s "
                     +"OR `dual_g` = %(noun)s  ORDER BY `singular_n` = %(noun)s DESC LIMIT 1")
    data_singular = {
      'noun': noun,
    }
    mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])
    cur = mysql.cursor(buffered=True,dictionary=True)
    cur.execute(select_singular,data_singular)
    nounDetails = cur.fetchone()
    cur.close()
    mysql.close()
    # get Gender value
    if(gender == None and nounDetails != None and nounDetails["gender"] != None): # if gender not given then take the noun gender from db if exist
        gender=nounDetails["gender"]
    elif(gender == None and (nounDetails == None or (nounDetails != None and nounDetails["gender"] == None))): # if gender not given and not in db then set default to 1 (male)
        gender=1

    chosenNoun=noun
    if (chosen_type=="singular"):
        # get singular Value
        chosenNoun=noun
        if (nounDetails == None or (nounDetails != None and nounDetails[singularByCase[case]] == None)):
            if gender == 0 :
                if not noun.endswith('ة'):
                    noun=noun + "ة"
            else:
                if noun.endswith('ة'):
                    noun=noun[:-1]
            chosenNoun=noun
        else:
            chosenNoun=nounDetails[singularByCase[case]]
    elif(chosen_type=="dual"):
        # get Dual Value
        if (nounDetails == None or (nounDetails != None and nounDetails[dualByCase[case]] == None)):
            chosenNoun=getManualNounDual(noun,case,gender)
        else:
            chosenNoun=nounDetails[dualByCase[case]]
        if(dual != None):
            chosenNoun=dual
    elif(chosen_type == "plural"):
        #get Plural value
        if (nounDetails == None or (nounDetails != None and nounDetails[pluralByCase[case]] == None)):
            chosenNoun=getManualNounPlural(noun,case,gender)
        else:
            chosenNoun=nounDetails[pluralByCase[case]]
        if(plural != None):
            chosenNoun=plural


    return chosenNoun


def getManualNounDual(noun,case,gender):
    if noun.endswith('ة') or noun.endswith('ه'):# most of the feminine noun ends with "ة", therefore it will treated as feminine sound plural
        if (case == "nominative"):
            return noun[:-1]+"تان"
        else:
            return noun[:-1]+"تين"
    else:
        if gender == 0:
            noun=noun+"ت"
        if (case == "nominative"): # if masculine and nominative add suffix "ون" to the end of the noun
            noun=noun+"ان"
        else: # if masculine and not nominative then add the suffix "ين" to the end of the noun
            noun = noun +"ين"
    return noun


def getManualNounPlural(noun,case,gender):
    if noun.endswith('ة') or noun.endswith('ه'):# most of the feminine noun ends with "ة", therefore it will treated as feminine sound plural
        return noun[:-1]+"ات"
    if (gender == 1 and case == "nominative"): # if masculine and nominative add suffix "ون" to the end of the noun
        noun=noun+"ون"
    elif(gender == 1 and case != "nominative"): # if masculine and not nominative then add the suffix "ين" to the end of the noun
        noun = noun +"ين"
    if (gender == 0): # if feminine and not ending with "ة" then add suffix "ات"
        noun=noun+"ات"
    return noun



def ar_inflectNoun(number, noun, case="nominative", gender = None, dual = None, plural = None):
    # check if the noun is Arabic word
    inflect_noun_printable=""
    noun=str(noun).strip()
    is_arabic_noun,noun,message=is_arabic_word(noun)
    if not is_arabic_noun:
        return { 'error':True,'message':' error in noun value: '+message}
    dual=str(dual).strip()
    if len(dual)==0:
        dual=None
    else:
        is_arabic_dual,dual,message=is_arabic_word(dual)
        if not is_arabic_dual:
            return { 'error':True,'message':' error in dual value: '+message}
    plural=str(plural).strip()
    if len(plural)==0:
        plural=None
    else:
        is_arabic_plural,plural,message=is_arabic_word(plural)
        if not is_arabic_plural:
            return { 'error':True,'message':' error in plural value: '+message}

    noun=str(noun).strip()
    if len(re.findall(r'[\u0600-\u06FF]+', noun)) <=0:
        return { 'error':True,'message':'word is not Arabic, type not supported'}
    else:
        try:
            noun=remove_diacritics(noun)
        except:
            return { 'error':True,'message':'the noun could not remove the diacritics '}
    #check if given gender is in string or int format and in one of these values (0,1,"m","f","male" or "female")
    try:
        gender = int(gender)
    except :
        gender=str(gender)
    if(gender is None or len(str(gender).strip())==0):
        gender=None
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
    #check if given case is a string and in one of these values ((nominative, accusative, genitive)
    if(case is None or len(str(case).strip())==0):
        case="nominative"
    else:
        if (isinstance(case,str) and case.strip().lower() in ["nominative","accusative","genitive"]):
            case=case.strip().lower()
        else:
            return False,"case value is not valid"

    try:
        number = int(number)
    except :
        number=str(number)
    if(number is None or len(str(number).strip())==0):
        number="singular"
    else:
        if isinstance(number,str) and (number in ["singular","dual","plural"]):
            number=str(number).strip().lower()

        elif isinstance(number,int):
            if number<0:
                number=number*-1

            if(number==1 or number == 0):
                number="singular"
            elif(number==2):
                number="dual"
            else:
                number="plural"

        else:
            return { 'error':True,'message':'Number type not supported'}
    inflect_noun_printable = get_noun_dual_plural_gender(noun,case,gender,dual,plural,number)
    if len(inflect_noun_printable)>0:
        return { 'result':inflect_noun_printable, 'error':False, 'message':""}
    else:
        return { 'error':True,'message':'No result found'}
