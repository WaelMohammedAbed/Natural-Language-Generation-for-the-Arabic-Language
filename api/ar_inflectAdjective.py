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




def getManualAdjectiveForm(adjective,case,gender,number_form):

    # most of the feminine adj ends with "ة", therefore it will treated as feminine sound plural
    if gender == 0 :
        if not adjective.endswith('ة'):
            adjective=adjective + "ة"
        if( number_form == "singular"):
            return adjective
        elif (number_form =="dual"):
            if (case == "nominative"):
                return adjective[:-1]+"تان"
            else:
                return adjective[:-1]+"تين"
        else:
            return adjective[:-1]+"ات"
    else:
        if adjective.endswith('ة'):
            adjective=adjective[:-1]
        if( number_form == "singular"):
            return adjective
        elif (number_form =="dual"):
            if (case == "nominative"): # if masculine and nominative add suffix "ان"
                adjective=adjective+"ان"
            elif(case != "nominative"): # if masculine and not nominative then add the suffix "ين"
                adjective = adjective +"ين"
        else:
            if (gender == 1 and case == "nominative"): # if masculine and nominative add suffix "ون"
                adjective=adjective+"ون"
            elif(gender == 1 and case != "nominative"): # if masculine and not nominative then add the suffix "ين"
                adjective = adjective +"ين"



    return adjective


def get_noun_modifiers(modifiers,
                        number_form = "singular",
                        case="nominative",
                        gender=True,
                        is_human=True,
                        agreement=True):
    column="f_"
    if gender:
        column="m_"
    column=column+number_form+"_"+case

    inflected_modifiers=[]
    for adjective in modifiers:
        select_adjective=("SELECT * FROM `modifiers` WHERE "
                          +"`root` = %(adjective)s OR "
                          +"`m_singular_nominative` = %(adjective)s OR "
                          +"`m_singular_accusative` = %(adjective)s OR "
                          +"`m_singular_genitive`  = %(adjective)s OR "
                          +"`m_dual_nominative` = %(adjective)s OR "
                          +"`m_dual_accusative` = %(adjective)s OR "
                          +"`m_dual_genitive`  = %(adjective)s OR "
                          +"`m_plural_nominative` = %(adjective)s OR "
                          +"`m_plural_accusative`  = %(adjective)s OR "
                          +"`m_plural_genitive`  = %(adjective)s OR "
                          +"`f_singular_nominative` = %(adjective)s OR "
                          +"`f_singular_accusative` = %(adjective)s OR "
                          +"`f_singular_genitive`  = %(adjective)s OR "
                          +"`f_dual_nominative` = %(adjective)s OR "
                          +"`f_dual_accusative`  = %(adjective)s OR "
                          +"`f_dual_genitive` = %(adjective)s OR "
                          +"`f_plural_nominative` = %(adjective)s OR "
                          +"`f_plural_accusative` = %(adjective)s OR "
                          +"`f_plural_genitive` = %(adjective)s ORDER BY `m_singular_nominative` = %(adjective)s DESC LIMIT 1")
        data_adjective = {
            'adjective': adjective,
        }
        cur = mysql.cursor(buffered=True,dictionary=True)

        cur.execute(select_adjective,data_adjective)
        adjectiveDetails = cur.fetchone()
        # deflected agreement condition
        if not is_human and not agreement and number_form== 'plural':
            #condition is true then take the feminine singular form
            column="f_singular_"+case

            #check if the value in the database
            if(adjectiveDetails == None or (adjectiveDetails != None and adjectiveDetails[column] == None)):
                #the value not in the database, therefore, change adj to feminine by adding "ة" suffix if it not found
                inflected_adjective=adjective
                if inflected_adjective[-1]!= "ه" and  inflected_adjective[-1]!= "ة":
                    inflected_adjective=inflected_adjective+"ة"
                inflected_modifiers.append(inflected_adjective)
                continue
            #else if it is in the database, then take it
            else:
                inflected_modifiers.append(adjectiveDetails[column])
                continue
        # if it it full agreement
        else:
            #check if the value in the database
            if(adjectiveDetails == None or (adjectiveDetails != None and adjectiveDetails[column] == None)):
                #the value not in the database, therefore, get it manually
                inflected_adjective=getManualAdjectiveForm(adjective,case,gender,number_form)
                inflected_modifiers.append(inflected_adjective)
                continue
            #else if it is in the database, then take it
            else:
                inflected_modifiers.append(adjectiveDetails[column])
                continue
    return inflected_modifiers



def inflectAdjectives(modifiers,number= "singular", case="nominative", gender = True, is_human = True, agreement = True):
    modifiers=str(modifiers).strip()
    if(len(modifiers)==0):
        return { 'error':True,'message':' modifiers is mandatory and can\'t be empty'}
    modifier_list=[]
    if "," in modifiers:
        for modifier in modifiers.split(","):
            is_arabic,word,message=is_arabic_word(modifier)
            if not is_arabic:
                return { 'error':True,'message':' error in modifiers value: '+message}
            modifier_list.append(word)
    else:
        is_arabic,word,message=is_arabic_word(modifiers)
        if not is_arabic:
            return { 'error':True,'message':' error in modifiers value: '+message}
        modifier_list.append(word)
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

    #check if given agreement is in string or int format and in one of these values (0,1,"m","f","male" or "female")
    try:
        agreement = int(agreement)
    except :
        agreement=str(agreement)
    if(agreement is None or len(str(agreement).strip())==0):
        agreement=True
    else:
        if (isinstance(agreement,str) and agreement.strip().lower() in ["fa","full","full agreement"]):
            agreement=True
        if (isinstance(agreement,str) and agreement.strip().lower() in ["da","deflected","deflected agreement"]):
            agreement=False
        elif (isinstance(agreement,int) and int(agreement) in [0,1]) or isinstance(agreement,bool):
            if(agreement):
                agreement=True
            else:
                agreement=False
        else:
            return { 'error':True, 'message':' agreement value is not valid'}

    #check if given is_human is in string or int format and in one of these values (0,1,"m","f","male" or "female")
    try:
        is_human = int(is_human)
    except :
        is_human=str(is_human)
    if(is_human is None or len(str(is_human).strip())==0):
        is_human=True
    else:
        if (isinstance(is_human,str) and is_human.strip().lower() in ["t","true","yes"]):
            is_human=True
        if (isinstance(is_human,str) and is_human.strip().lower() in ["f","false","no"]):
            agreement=False
        elif (isinstance(is_human,int) and int(is_human) in [0,1]) or isinstance(is_human,bool):
            if(is_human):
                is_human=True
            else:
                is_human=False
        else:
            return { 'error':True, 'message':' is_human value is not valid'}


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

    inflected_modifiers_list=get_noun_modifiers(modifier_list,number,case,gender,is_human,agreement)
    if len(inflected_modifiers_list)>0:

        if len(inflected_modifiers_list)>1:
            inflected_modifiers=" و ".join(inflected_modifiers_list)
        else:
            inflected_modifiers=inflected_modifiers_list[0]
        return { 'result':inflected_modifiers, 'error':False, 'message':""}
    else:
        return { 'error':True,'message':'No result found'}
