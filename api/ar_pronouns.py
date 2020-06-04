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



def get_choosen_pronoun(gender,number,person,pronoun_type):

    cur = mysql.cursor(buffered=True,dictionary=True)
    select_pronoun=("SELECT `pronoun` FROM `personal_pronouns` WHERE "
                    +" `gender`= %(gender)s "
                    +"AND `number`= %(number)s "
                    +"AND `person`= %(person)s "
                    +"AND `type`= %(type)s ")
    data_pronoun = {
      'gender': gender,
      'number': number,
      'person': person,
      'type': pronoun_type
    }
    cur.execute(select_pronoun,data_pronoun)
    resultDetails = cur.fetchone()



    return resultDetails["pronoun"]

def get_ar_pronoun(number, gender, person, pronoun_type, word,is_person):
    result =""

    if pronoun_type == "subject":
        pronoun=get_choosen_pronoun(gender,number,person,pronoun_type)
        result = pronoun+" "+word
    elif pronoun_type == "possessive":
        pronoun=get_choosen_pronoun(gender,number,person,pronoun_type)

        # If the noun in its dual form or in its masculine plural form that means they
        # ends with these suffixes ( ان, ين, ون). In this case the “ن” is removed when
        # adding a pronoun suffix to it. Moreover, if the added possessive pronoun is the
        # first person singular form, then, both suffixes “ون” and “ين” has to be replaced
        # with the suffix “ـي” only
        if word.endswith("ان") or word.endswith("ين") or word.endswith("ون"):
            if person==1 and number==1 and (word.endswith("ون") or word.endswith("ين")):
                word=word[:-2]
            else:
                word=word[:-1]
        # it is not allowed in Arabic to use a two consecutive same vowel and they should
        # merge in one
        if pronoun == "ي" and word.endswith("ي"):
            word=word[:-1]
        # If the noun ends with the letter “ة” (taa’ marbuuta). When the suffix pronoun
        # added, this character must be changed to “ت” (taa’ tawila) then add the suffix
        if word.endswith('ة'):
            word=word[:-1]+"ت"
        result = word+pronoun
    elif pronoun_type == "object":
        pronoun=get_choosen_pronoun(gender,number,person,pronoun_type)
        # if these pronouns added to a verb in its 2nd person, masculine, plural, past tense
        # and the last two letters are “تم” (tum), then the vowel “و” is added to the end
        # of the verb before adding the suffix
        if gender==1 and number == 3 and person == 2 and word.endswith("تم"):
            word=word+"و"
        elif word in ["ل","من","في","عن"] and pronoun == "ني":
            pronoun="ي"
        # the three letters preposition “على” or "إلى", its last letter change to “ي”
        # when adding the suffixes pronouns
        elif word in ["على","الى","إلى"]:
            word= word[:-1]+"ي"
        # it is not allowed in Arabic to use a two consecutive same vowel and they should
        # merge in one and with prepositions pronoun ي is used instead of ني
        if pronoun == "ي" and word.endswith("ي"):
            word=word[:-1]
        result = word+pronoun
    elif pronoun_type == "accusative_object":
        pronoun=get_choosen_pronoun(gender,number,person,"object")
        # it is independent pronouns, can be inflected by adding the possessive pronoun
        # as a suffix to “ايا” “iya”  to generate object pronouns
        if pronoun == "ني":
            pronoun = "ي"
        pronoun = "إيا"+pronoun
        result = word+" "+pronoun
    elif pronoun_type == "reflexive":
        pronoun=get_choosen_pronoun(gender,number,person,"possessive")
        # to inflect reflexive pronoun in Arabic, the word “نفس” is used with possessive pronoun suffix
        pronoun = "نفس"+pronoun
        result = word+" "+pronoun



    return result


def check_params(number=3, gender = 1, person = 3, pronoun_type = "subject", word=None, is_person= "True"):


    #check if given number is in string or int format and in one of these values (1,2,3,"singular","dual" or "plural")
    try:
        number = int(number)
    except :
        number=str(number)
    if(number is None or len(str(number).strip())==0):
        number=1
    else:
        if (isinstance(number,str) and number.strip().lower() in ["singular","dual","plural"]):
            str_to_number={"singular":1,"dual":2,"plural":3}
            number=str_to_number[number.strip().lower()]
        elif (isinstance(number,int)):
            number=int(number)
            if(number < 0):
                number= number * -1
            if(number == 0):
                number=1
            elif(number>3):
                number=3
        else:
            return False,"number value is not valid",number, gender, person, pronoun_type, word, is_person

    #check if given gender is in string or int format and in one of these values (0,1,"m","f","male" or "female")
    try:
        gender = int(gender)
    except :
        gender=str(gender)
    if(gender is None or len(str(gender).strip())==0):
        gender=1
    else:
        if (isinstance(gender,str) and gender.strip().lower() in ["male","m"]):
            gender=1
        elif (isinstance(gender,str) and gender.strip().lower() in ["female","f"]):
            gender=0
        elif (isinstance(gender,int) and int(gender) in [0,1]) or isinstance(gender,bool):
            if(gender):
                gender=1
            else:
                gender=0
        else:
            return False,"gender value is not valid",number, gender, person, pronoun_type, word, is_person

    #check if given person is in int format and in one of these values (1,2,3)
    if(person is None or len(str(person).strip())==0):
        person=3
    try:
        person = int(person)
        if (person in [1,2,3]):
            person=int(person)
        else:
            return False,"person value is not valid",number, gender, person, pronoun_type, word, is_person

    except :
        return False,"person value is not valid",number, gender, person, pronoun_type, word, is_person

    #check if given pronoun_type is a string and in one of these values (subject, object, reflexive, possessive, or accusative object)
    if(pronoun_type is None or len(str(pronoun_type).strip())==0):
        pronoun_type="subject"
    if (isinstance(pronoun_type,str) and pronoun_type.strip().lower() in ["subject","object","reflexive","possessive","accusative_object"]):
        pronoun_type=pronoun_type.strip().lower()
    else:
        return False,"pronoun type value is not valid",number, gender, person, pronoun_type, word, is_person


    #check if given word is in string format, Arabic and with with at least one lettre if pronoun type is possessive or object
    if   isinstance(word,str) and len(word)>0 and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(word)))==1:
        word=remove_diacritics(word) # remove diacrtics if given
    elif  pronoun_type not in ["possessive","object"]: # if the word is not in arabic just ignore it
        word=""
    else:
        return False,"Word value is not valid",number, gender, person, pronoun_type, word, is_person

    #check if given is_person is in string or boolean format and in one of these values (0,1,"t","f","true" or "false")
    if(is_person is None or len(str(is_person).strip())==0):
        is_person=True
    if (isinstance(is_person,str) and is_person.strip().lower() in ["true","t","1"]):
        is_person=True
    elif (isinstance(is_person,str) and is_person.strip().lower() in ["false","f","0"]):
        is_person=False
    elif (isinstance(is_person,int) and int(is_person) in [0,1]) or isinstance(is_person,bool):
        is_person=isinstance(is_person,bool)
    else:
        return False,"is_person value is not valid",number, gender, person, pronoun_type, word, is_person

    #check conflict between parameters
    #dual or number 2 can’t be used with the 1st person, therefore, in this case the pronoun of the plural first person will be used
    if person ==1 and number==2:
        number=3
    #for nonhuman plurals in Arabic language the singular feminine in its third person form is used without considering the gender
    if not is_person and number==3:
        number=1
        gender=0
        person=3


    return True,"",number, gender, person, pronoun_type, word, is_person

def ar_pronoun(number=3, gender = 1, person = 3, pronoun_type = "subject", word=None, is_person= "True"):
    # check if params' values are valid
    status,message,number, gender, person, pronoun_type, word, is_person = check_params(number, gender, person, pronoun_type, word, is_person)

    if status:
        ar_pronoun_printable = get_ar_pronoun(number, gender, person, pronoun_type, word, is_person)
        return { 'result':ar_pronoun_printable, 'error':False, 'message':""}
    else:
        return { 'result':"", 'error':True, 'message':message}
