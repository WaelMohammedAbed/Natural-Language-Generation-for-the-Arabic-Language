import mysql.connector as MySQL
from numeral_names import numeral_names
import yaml



# Configure db
db = yaml.safe_load(open('db.yaml'))

mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])

def get_noun_dual_plural_gender(noun,case="nominative",gender = None,dual=None,plural=None,chosen_type="singular"):
    pluralByCase={'accusative': "plural_a", 'nominative': "plural_n", 'genitive':"plural_g"}
    dualByCase={'accusative': "dual_a", 'nominative': "dual_n", 'genitive':"dual_g"}
    singularByCase={'accusative': "singular_a", 'nominative': "singular_n", 'genitive':"singular_g"}
    cur = mysql.cursor(buffered=True,dictionary=True)
    select_singular=("SELECT * FROM `nouns_2` WHERE "
                     +"`singular_a` = %(noun)s "
                     +"OR `singular_n` = %(noun)s "
                     +"OR `singular_g` = %(noun)s "
                     +"OR `plural_a` = %(noun)s "
                     +"OR `plural_n` = %(noun)s "
                     +"OR `plural_g` = %(noun)s "
                     +"OR `dual_a` = %(noun)s "
                     +"OR `dual_n` = %(noun)s "
                     +"OR `dual_g` = %(noun)s ")
    data_singular = {
      'noun': noun,
    }
    cur.execute(select_singular,data_singular)
    nounDetails = cur.fetchone()

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
            if nounDetails['singular_n'] is not None:
                chosenNoun=nounDetails['singular_n']
            elif nounDetails['singular_a'] is not None:
                chosenNoun=nounDetails['singular_a']
            elif nounDetails['singular_g'] is not None:
                chosenNoun=nounDetails['singular_g']
            else:
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



def inflectNoun(count, noun, case="nominative", gender = None, dual = None, plural = None):
    if isinstance(count,str) and (count in ["singular","dual","plural"]):
        inflect_noun_printable = get_noun_dual_plural_gender(noun,case,gender,dual,plural,count)
    elif isinstance(count,int) and int(count)>0:
        if(count==1):
            count="singular"
        elif(count==2):
            count="dual"
        else:
            count="plural"
        inflect_noun_printable = get_noun_dual_plural_gender(noun,case,gender,dual,plural,count)
    else:
        return { 'error':True,'message':'type not supported'}

    if len(inflect_noun_printable)>0:
        return { 'result':inflect_noun_printable, 'error':False, 'message':""}
    else:
        return { 'error':'not found'}

# ex 1 all default values
count=3 # "dual", "plural" or a number (ex: 12)
noun="جائزة"
case="genitive" #"nominative", "accusative" or "genitive"
gender = None # 1 male , 0 female
dual = None # the dual form of the noun
plural = None # the plural form of the noun

noun=inflectNoun(count,noun,case,gender,dual,plural)
print(noun)
