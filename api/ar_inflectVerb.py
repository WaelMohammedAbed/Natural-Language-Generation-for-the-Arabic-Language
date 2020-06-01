import mysql.connector as MySQL
import re
import yaml

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
        #print(text)
        text = re.sub(arabic_diacritics, '', text)
    except:
        #print("error",text)
        return text
        
    return text





# Configure db
db = yaml.safe_load(open('db.yaml'))

mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])



def get_choosen_verb_inflection(word,choosen_verb_inflection):

    cur = mysql.cursor(buffered=True,dictionary=True)
    select_singular=("SELECT `"+choosen_verb_inflection+"` FROM `verbs_inflections` WHERE "
                     +"`verb_root` = %(word)s  ")
    data_singular = {
      'word': word,
    }
    cur.execute(select_singular,data_singular)
    resultDetails = cur.fetchone()
    if resultDetails != None and resultDetails[choosen_verb_inflection] != None:
        return resultDetails[choosen_verb_inflection]
    else:
        return "not found"

def get_ar_inflectVerb(word, number, gender, person, voice, mood_tense,choosen_verb_inflection):
    # TO DO: manually inflect verb if it is not found in the db
    return get_choosen_verb_inflection(word,choosen_verb_inflection)


def check_params(word, number=3, gender = 1, person = 3, voice = "active", mood_tense = "past"):
        #check if given verb is in string format, Arabic and with more than one lettre
    if isinstance(word,str) and len(word)>1 and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(word)))==1:
        word=remove_diacritics(word) # remove diacrtics if given
    else:
        return False,"Verb value is not valid"
    
    #check if given number is in string or int format and in one of these values (1,2,3,"singular","dual" or "plural")
    if (isinstance(number,str) and number.strip().lower() in ["singular","dual","plural"]):
        number=number.strip().lower()
    elif (isinstance(number,int) and int(number) in [1,2,3]):
        number_to_str=["singular","dual","plural"]
        number=number_to_str[int(number)-1]
    else:
        return False,"number value is not valid"
    
    #check if given gender is in string or int format and in one of these values (0,1,"m","f","male" or "female")
    if (isinstance(gender,str) and gender.strip().lower() in ["male","female","m","f"]):
        gender=gender.strip().lower()[0]
    elif (isinstance(gender,int) and int(gender) in [0,1]) or isinstance(gender,bool):
        if(gender):
            gender="m"
        else:
            gender="f"
    else:
        return False,"gender value is not valid"
    
    #check if given person is in int format and in one of these values (1,2,3)
    if (isinstance(person,int) and int(person) in [1,2,3]):
        person=int(person)
    else:
        return False,"person value is not valid"
    
  
    #check if given mood_tense is a string and in one of these values ((“past”, ”none_past”, “subjunctive”, “jussive” or “imperative”)
    if (isinstance(mood_tense,str) and mood_tense.strip().lower() in ["past","none_past","subjunctive","jussive","imperative"]):
        mood_tense=mood_tense.strip().lower()
    else:
        return False,"mood_tense value is not valid"
    
    #check if given voice is a string and in one of these values ("active","passive")
    if (isinstance(voice,str) and voice.strip().lower() in ["active","passive"]):
        voice=voice.strip().lower()
    else:
        return False,"voice value is not valid"
    
    #check conflict between parameters
    if(mood_tense=="imperative" and person != 2):
        return False,"imperative mood_tense can use only with 2nd person"
    if(mood_tense=="imperative" and voice=="passive"):
        return False,"imperative mood_tense can use only with passive voice"
    if(number=="dual" and person==1):
        return False,"Dual Number can not be used with 1st person"
    
    choosen_verb_inflection=voice+"_"+mood_tense+"_"+number+"_"+str(person)+"_"+gender
    
    return True,choosen_verb_inflection
def ar_inflectVerb(word, number=3, gender = 1, person = 3, voice = "active", mood_tense = "past"):
    # check if params' values are valid
    status,result = check_params(word, number, gender, person, voice, mood_tense)
    
    if status:
        choosen_verb_inflection=result
        ar_inflectVerb_printable = get_ar_inflectVerb(word, number, gender, person, voice, mood_tense,choosen_verb_inflection)
        return { 'result':ar_inflectVerb_printable, 'error':False, 'message':""}
        #return { 'result':countable_noun_printable, 'error':False, 'message':""}
    else:
        return { 'result':"", 'error':True, 'message':result}
    
    