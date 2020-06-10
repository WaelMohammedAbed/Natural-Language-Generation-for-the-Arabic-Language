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
        text = re.sub(arabic_diacritics, '', text)
    except:
        return text

    return text





# Configure db
db = yaml.safe_load(open('db.yaml'))




def get_choosen_verb_inflection(word,choosen_verb_inflection):


    select_singular=("SELECT `"+choosen_verb_inflection+"` FROM `verbs_inflections` WHERE "
                     +" `verb_root` = %(value)s "
                    +" OR `form_number` = %(value)s "
                    +" OR `active_past_singular_1_m` = %(value)s "
                    +" OR `active_past_singular_1_f` = %(value)s "
                    +" OR `active_past_singular_2_m` = %(value)s "
                    +" OR `active_past_singular_2_f` = %(value)s "
                    +" OR `active_past_singular_3_m` = %(value)s "
                    +" OR `active_past_singular_3_f` = %(value)s "
                    +" OR `active_past_dual_2_m` = %(value)s "
                    +" OR `active_past_dual_2_f` = %(value)s "
                    +" OR `active_past_dual_3_m` = %(value)s "
                    +" OR `active_past_dual_3_f` = %(value)s "
                    +" OR `active_past_plural_1_m` = %(value)s "
                    +" OR `active_past_plural_1_f` = %(value)s "
                    +" OR `active_past_plural_2_m` = %(value)s "
                    +" OR `active_past_plural_2_f` = %(value)s "
                    +" OR `active_past_plural_3_m` = %(value)s "
                    +" OR `active_past_plural_3_f` = %(value)s "
                    +" OR `active_none_past_singular_1_m` = %(value)s "
                    +" OR `active_none_past_singular_1_f` = %(value)s "
                    +" OR `active_none_past_singular_2_m` = %(value)s "
                    +" OR `active_none_past_singular_2_f` = %(value)s "
                    +" OR `active_none_past_singular_3_m` = %(value)s "
                    +" OR `active_none_past_singular_3_f` = %(value)s "
                    +" OR `active_none_past_dual_2_m` = %(value)s "
                    +" OR `active_none_past_dual_2_f` = %(value)s "
                    +" OR `active_none_past_dual_3_m` = %(value)s "
                    +" OR `active_none_past_dual_3_f` = %(value)s "
                    +" OR `active_none_past_plural_1_m` = %(value)s "
                    +" OR `active_none_past_plural_1_f` = %(value)s "
                    +" OR `active_none_past_plural_2_m` = %(value)s "
                    +" OR `active_none_past_plural_2_f` = %(value)s "
                    +" OR `active_none_past_plural_3_m` = %(value)s "
                    +" OR `active_none_past_plural_3_f` = %(value)s "
                    +" OR `active_subjunctive_singular_1_m` = %(value)s "
                    +" OR `active_subjunctive_singular_1_f` = %(value)s "
                    +" OR `active_subjunctive_singular_2_m` = %(value)s "
                    +" OR `active_subjunctive_singular_2_f` = %(value)s "
                    +" OR `active_subjunctive_singular_3_m` = %(value)s "
                    +" OR `active_subjunctive_singular_3_f` = %(value)s "
                    +" OR `active_subjunctive_dual_2_m` = %(value)s "
                    +" OR `active_subjunctive_dual_2_f` = %(value)s "
                    +" OR `active_subjunctive_dual_3_m` = %(value)s "
                    +" OR `active_subjunctive_dual_3_f` = %(value)s "
                    +" OR `active_subjunctive_plural_1_m` = %(value)s "
                    +" OR `active_subjunctive_plural_1_f` = %(value)s "
                    +" OR `active_subjunctive_plural_2_m` = %(value)s "
                    +" OR `active_subjunctive_plural_2_f` = %(value)s "
                    +" OR `active_subjunctive_plural_3_m` = %(value)s "
                    +" OR `active_subjunctive_plural_3_f` = %(value)s "
                    +" OR `active_jussive_singular_1_m` = %(value)s "
                    +" OR `active_jussive_singular_1_f` = %(value)s "
                    +" OR `active_jussive_singular_2_m` = %(value)s "
                    +" OR `active_jussive_singular_2_f` = %(value)s "
                    +" OR `active_jussive_singular_3_m` = %(value)s "
                    +" OR `active_jussive_singular_3_f` = %(value)s "
                    +" OR `active_jussive_dual_2_m` = %(value)s "
                    +" OR `active_jussive_dual_2_f` = %(value)s "
                    +" OR `active_jussive_dual_3_m` = %(value)s "
                    +" OR `active_jussive_dual_3_f` = %(value)s "
                    +" OR `active_jussive_plural_1_m` = %(value)s "
                    +" OR `active_jussive_plural_1_f` = %(value)s "
                    +" OR `active_jussive_plural_2_m` = %(value)s "
                    +" OR `active_jussive_plural_2_f` = %(value)s "
                    +" OR `active_jussive_plural_3_m` = %(value)s "
                    +" OR `active_jussive_plural_3_f` = %(value)s "
                    +" OR `active_imperative_singular_2_m` = %(value)s "
                    +" OR `active_imperative_singular_2_f` = %(value)s "
                    +" OR `active_imperative_dual_2_m` = %(value)s "
                    +" OR `active_imperative_dual_2_f` = %(value)s "
                    +" OR `active_imperative_plural_2_m` = %(value)s "
                    +" OR `active_imperative_plural_2_f` = %(value)s "

                    +" OR `passive_past_singular_1_m` = %(value)s "
                    +" OR `passive_past_singular_1_f` = %(value)s "
                    +" OR `passive_past_singular_2_m` = %(value)s "
                    +" OR `passive_past_singular_2_f` = %(value)s "
                    +" OR `passive_past_singular_3_m` = %(value)s "
                    +" OR `passive_past_singular_3_f` = %(value)s "
                    +" OR `passive_past_dual_2_m` = %(value)s "
                    +" OR `passive_past_dual_2_f` = %(value)s "
                    +" OR `passive_past_dual_3_m` = %(value)s "
                    +" OR `passive_past_dual_3_f` = %(value)s "
                    +" OR `passive_past_plural_1_m` = %(value)s "
                    +" OR `passive_past_plural_1_f` = %(value)s "
                    +" OR `passive_past_plural_2_m` = %(value)s "
                    +" OR `passive_past_plural_2_f` = %(value)s "
                    +" OR `passive_past_plural_3_m` = %(value)s "
                    +" OR `passive_past_plural_3_f` = %(value)s "
                    +" OR `passive_none_past_singular_1_m` = %(value)s "
                    +" OR `passive_none_past_singular_1_f` = %(value)s "
                    +" OR `passive_none_past_singular_2_m` = %(value)s "
                    +" OR `passive_none_past_singular_2_f` = %(value)s "
                    +" OR `passive_none_past_singular_3_m` = %(value)s "
                    +" OR `passive_none_past_singular_3_f` = %(value)s "
                    +" OR `passive_none_past_dual_2_m` = %(value)s "
                    +" OR `passive_none_past_dual_2_f` = %(value)s "
                    +" OR `passive_none_past_dual_3_m` = %(value)s "
                    +" OR `passive_none_past_dual_3_f` = %(value)s "
                    +" OR `passive_none_past_plural_1_m` = %(value)s "
                    +" OR `passive_none_past_plural_1_f` = %(value)s "
                    +" OR `passive_none_past_plural_2_m` = %(value)s "
                    +" OR `passive_none_past_plural_2_f` = %(value)s "
                    +" OR `passive_none_past_plural_3_m` = %(value)s "
                    +" OR `passive_none_past_plural_3_f` = %(value)s "
                    +" OR `passive_subjunctive_singular_1_m` = %(value)s "
                    +" OR `passive_subjunctive_singular_1_f` = %(value)s "
                    +" OR `passive_subjunctive_singular_2_m` = %(value)s "
                    +" OR `passive_subjunctive_singular_2_f` = %(value)s "
                    +" OR `passive_subjunctive_singular_3_m` = %(value)s "
                    +" OR `passive_subjunctive_singular_3_f` = %(value)s "
                    +" OR `passive_subjunctive_dual_2_m` = %(value)s "
                    +" OR `passive_subjunctive_dual_2_f` = %(value)s "
                    +" OR `passive_subjunctive_dual_3_m` = %(value)s "
                    +" OR `passive_subjunctive_dual_3_f` = %(value)s "
                    +" OR `passive_subjunctive_plural_1_m` = %(value)s "
                    +" OR `passive_subjunctive_plural_1_f` = %(value)s "
                    +" OR `passive_subjunctive_plural_2_m` = %(value)s "
                    +" OR `passive_subjunctive_plural_2_f` = %(value)s "
                    +" OR `passive_subjunctive_plural_3_m` = %(value)s "
                    +" OR `passive_subjunctive_plural_3_f` = %(value)s "
                    +" OR `passive_jussive_singular_1_m` = %(value)s "
                    +" OR `passive_jussive_singular_1_f` = %(value)s "
                    +" OR `passive_jussive_singular_2_m` = %(value)s "
                    +" OR `passive_jussive_singular_2_f` = %(value)s "
                    +" OR `passive_jussive_singular_3_m` = %(value)s "
                    +" OR `passive_jussive_singular_3_f` = %(value)s "
                    +" OR `passive_jussive_dual_2_m` = %(value)s "
                    +" OR `passive_jussive_dual_2_f` = %(value)s "
                    +" OR `passive_jussive_dual_3_m` = %(value)s "
                    +" OR `passive_jussive_dual_3_f` = %(value)s "
                    +" OR `passive_jussive_plural_1_m` = %(value)s "
                    +" OR `passive_jussive_plural_1_f` = %(value)s "
                    +" OR `passive_jussive_plural_2_m` = %(value)s "
                    +" OR `passive_jussive_plural_2_f` = %(value)s "
                    +" OR `passive_jussive_plural_3_m` = %(value)s "
                    +" OR `passive_jussive_plural_3_f` = %(value)s ORDER BY `verb_root` = %(value)s DESC LIMIT 1")
    data_singular = {
      'value': word,
    }
    mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])
    cur = mysql.cursor(buffered=True,dictionary=True)
    cur.execute(select_singular,data_singular)
    resultDetails = cur.fetchone()
    cur.close()
    mysql.close()
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
    try:
        number = int(number)
    except :
        number=str(number)
    if(number is None or len(str(number).strip())==0):
        number="plural"
    else:
        if (isinstance(number,str) and number.strip().lower() in ["singular","dual","plural"]):
            number=number.strip().lower()
        elif (isinstance(number,int)):
            number=int(number)
            if(number<0):
                number=number * -1
            if(number==1 or number == 0):
                number="singular"
            elif(number==2):
                number="dual"
            else:
                number="plural"

        else:
            return False,"number value is not valid"

    #check if given gender is in string or int format and in one of these values (0,1,"m","f","male" or "female")
    try:
        gender = int(gender)
    except :
        gender=str(gender)
    if(gender is None or len(str(gender).strip())==0):
        gender="m"
    else:
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
    if(person is None or len(str(person).strip())==0):
        person=3
    else:
        try:
            person = int(person)
            if person not in [1,2,3]:
                return False,"person value is not valid"

        except :
            return False,"person value is not valid"

    #check if given mood_tense is a string and in one of these values ((“past”, ”none_past”, “subjunctive”, “jussive” or “imperative”)
    if(mood_tense is None or len(str(mood_tense).strip())==0):
        mood_tense="past"
    else:
        if (isinstance(mood_tense,str) and mood_tense.strip().lower() in ["past","none_past","subjunctive","jussive","imperative"]):
            mood_tense=mood_tense.strip().lower()
        else:
            return False,"mood_tense value is not valid"

    #check if given voice is a string and in one of these values ("active","passive")
    if(voice is None or len(str(voice).strip())==0):
        voice="active"
    else:
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
