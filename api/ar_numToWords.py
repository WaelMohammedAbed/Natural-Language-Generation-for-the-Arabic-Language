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

def get_noun_dual_plural_gender(noun,case="nominative",gender = None,numbers_type=None,plural=None,chosen_type="singular",modifiers=[],agreement=True):
    if len(noun)==0:
        return "",gender

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
                     +"OR `dual_g` = %(noun)s  ORDER BY `singular_n` = %(noun)s DESC LIMIT 1")
    data_singular = {
      'noun': noun,
    }
    cur.execute(select_singular,data_singular)
    nounDetails = cur.fetchone()
    # get Gender value
    if(gender == None and nounDetails != None and nounDetails["gender"] != None): # if gender not given then take the noun gender from db if exist
        gender=nounDetails["gender"]
    elif (gender == None and (nounDetails == None or (nounDetails != None and nounDetails["gender"] == None))): # if gender not given and not in db then set default to 1 (male)
        gender=1

    chosenNoun=noun
    if (chosen_type=="singular"):
        # get singular Value
        chosenNoun=noun
        if (nounDetails == None):
            chosenNoun=noun
        elif (nounDetails != None and nounDetails[singularByCase[case]] == None):
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

    elif(chosen_type == "plural"):
        #get Plural value
        if (nounDetails == None or (nounDetails != None and nounDetails[pluralByCase[case]] == None)):
            chosenNoun=getManualNounPlural(noun,case,gender)
        else:
            chosenNoun=nounDetails[pluralByCase[case]]
        if(plural != None):
            chosenNoun=plural

    if numbers_type == "ordinal":
        chosenNoun="ال"+chosenNoun

    return chosenNoun,gender #numbers_type,plural,gender,is_human





def get_numeral(number,case,gender,numbers_type):
    table_name="numerals"
    if(numbers_type=="ordinal"):
        table_name="ordinal_numerals"

    select_numeral=("SELECT `numeral` FROM `"+table_name+"` WHERE `number` = %(number)s AND  `gender` = %(gender)s AND `noun_case` = %(noun_case)s")
    data_numeral = {
      'number': number,
      'noun_case': case,
      'gender': gender,
    }
    cur = mysql.cursor(buffered=True)
    cur.execute(select_numeral,data_numeral)
    numeralDetails = cur.fetchone()
    return numeralDetails[0]



def simplex_singular_numeral(number, noun, case="nominative", gender = None, numbers_type = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    chosen_type="singular"
    if(number==2):
        chosen_type="dual"

    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,chosen_type,modifiers,agreement)
    numeral=get_numeral(number,case,gender,numbers_type)
    numeralNumber=2
    ordinal_numeral_names = ["ال"+x for x in numeral_names]
    if(noun in numeral_names or noun in ordinal_numeral_names):
        numeral=""
        numeralNumber=""
    if(number ==1 and ((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly")):    #
        if numbers_type == "ordinal":
            return numeral,chosenNoun,0 # numeral,noun, numeral_index
        else:
            return chosenNoun,numeral,1 # noun, numeral, numeral_index
    elif(number ==1 and ((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly")):    #
        if numbers_type == "ordinal":
            return "1",chosenNoun,0 # numeral,noun, numeral_index
        else:
            return chosenNoun,"1",1 # noun, numeral, numeral_index
    elif(number ==2 and ((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly")):    #
        if numbers_type == "ordinal":
            return numeral,chosenNoun,0 # numeral,noun, numeral_index
        else:
            return chosenNoun,numeral,1 # noun, numeral, numeral_index
    elif(number ==2 and ((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly")):    #
        if numbers_type == "ordinal":
            return numeralNumber,chosenNoun,0 # noun, numeral, numeral_index
        else:
            return chosenNoun,numeralNumber,1 # noun, numeral, numeral_index

    else:
        return "error"

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

def simplex_added_numeral(number, noun, case="nominative", gender = None, numbers_type = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    chosen_type="plural"
    if number == 10:
        chosen_type="singular"
    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,chosen_type,modifiers,agreement)

    if numbers_type == "cardinal":
        gender = 1 - gender # toggle the gender as the numeral takes the opposite gender of the noun in added numeral group


    numeralDetails=get_numeral(number,case,gender,numbers_type)
    if(number >2 and number <=10 and ((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,numeralDetails,1 # noun, numeral, numeral_index
        else:
            return numeralDetails,chosenNoun,0 # numeral, noun, numeral_index

    elif(number >2 and number <=10 and ((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,str(number),1 # noun, numeral, numeral_index
        else:
            return str(number),chosenNoun,0 # numeral, noun, numeral_index

    else:
        return "error"

def getManualNounPlural(noun,case,gender):
    if gender == 0 :
        if not noun.endswith('ة'):
            return noun+"ات"
        else:
            return noun[:-1]+"ات"
    else:
        if noun.endswith('ة'):
            noun=noun[:-1]
        if ( case == "nominative"): # if masculine and nominative add suffix "ون"
            noun=noun+"ون"
        elif( case != "nominative"): # if masculine and not nominative then add the suffix "ين"
            noun = noun +"ين"

    return noun

# Group Compound nouns
def compound_numeral_first_subgroup(number, noun, case="nominative", gender = None, numbers_type = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):

    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,"singular",modifiers,agreement)



    numeralDetails=get_numeral(number,case,gender,numbers_type)
    if(number >10 and number <=12 and ((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,numeralDetails,1 # noun, numeral, numeral_index
        else:
            return numeralDetails,chosenNoun,0 # numeral, noun, numeral_index

    elif(number >10 and number <=12 and ((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,str(number),1 # noun, numeral, numeral_index
        else:
            return str(number),chosenNoun,0 # numeral, noun, numeral_index

    else:
        return "error"


def compound_numeral_second_subgroup(number, noun, case="nominative", gender = None, numbers_type = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):

    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,"singular",modifiers,agreement)

    numeralDetails=get_numeral(10,case,gender,"cardinal")

    if numbers_type == "cardinal":
        gender=1-gender

    unit=number%10

    unitNumeralDetails=get_numeral(unit,case,gender,numbers_type)




    if(number >12 and number <=19 and ((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,unitNumeralDetails+" "+numeralDetails,1 # noun, numeral, numeral_index
        else:
            return unitNumeralDetails+" "+numeralDetails,chosenNoun,0 # numeral, noun, numeral_index

    elif(number >12 and number <=19 and ((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,str(number),1 # noun, numeral, numeral_index
        else:
            return str(number),chosenNoun,0 # numeral, noun, numeral_index

    else:
        return "error"

def complex_numeral_first_subgroup(number, noun, case="nominative", gender = None, numbers_type = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):

    digits=[int(x) for x in str(number)]
    units=digits[1]
    units_numeral=""
    if(int(units)>0):
        if numbers_type == "ordinal" and int(units) == 1:
            unitsDetails=numToWords(11, noun, case, gender, numbers_type, plural, number_format, zero_format)
            unitsNumeral=unitsDetails[unitsDetails[-1]].split(" ")[0]
            units_numeral=unitsNumeral+" و "
        else:
            unitsDetails=numToWords(units, noun, case, gender, numbers_type, plural, number_format, zero_format)
            units_numeral=unitsDetails[unitsDetails[2]]+" و "
    tens=digits[0]


    if(tens==2):
        tens=(tens-1)*10


    tensDetails=numToWords(tens, "", "nominative", 0)
    tens_numeral=getManualNounPlural(tensDetails[tensDetails[2]],case,1)

    if(numbers_type=="ordinal"):
        tens_numeral="ال"+tens_numeral


    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,"singular",modifiers,agreement)



    if(number >19 and number <=99 and ((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,units_numeral+tens_numeral,1 # noun, numeral, numeral_index
        else:
            return units_numeral+tens_numeral,chosenNoun,0 # numeral, noun, numeral_index

    elif(number >19 and number <=99 and ((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly")):    #
        if numbers_type == "ordinal":
            return chosenNoun,str(number),1 # noun, numeral, numeral_index
        else:
            return str(number),chosenNoun,0 # numeral, noun, numeral_index
    else:
        return "error"

def complex_numeral_second_subgroup(number, noun, case="nominative", gender = None, numbers_type = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    threeDigits=[]
    threeDigits.append(str(number)[-3:])
    for i in range(3, len(str(number)), 3):
        threeDigits.append(str(number)[-3-i:-i])
    numerals=numeral_names
    complex_numeral=[]
    for index,digits in enumerate(threeDigits):
        if(index==0):
            third_digit_numeral=""
            third_digit_numeral_list=[]
            numerals_hunderd=numerals[0]
            temp_gender=gender
            if numbers_type == "ordinal":

                numerals_hunderd="ال"+numerals_hunderd
                temp_numerals_hunderd="ال" + numerals_hunderd
                temp_gender=0
            if(len(digits)==3 and int(digits[0])==1):

                third_digit_numeral=numerals_hunderd
            elif(len(digits)==3 and int(digits[0])==2):

                third_digit_numeral=get_noun_dual_plural_gender(numerals_hunderd,case,0,None,None,"dual")[0]
            elif(len(digits)==3 and int(digits[0])>2):

                third_digit_numeral_list=numToWords(int(digits[0]), numerals[0], case, temp_gender, numbers_type, numerals[0], number_format, zero_format)

                third_digit_numeral=third_digit_numeral_list[0]+" "+third_digit_numeral_list[1]

            second_first_digits=int(digits[1]+digits[2])
            second_first_digit_numeral_list=["","",""]
            if (numbers_type=="ordinal"):

                if(second_first_digits>0):
                    if len (third_digit_numeral)>0:
                        third_digit_numeral="بعد "+third_digit_numeral
                    second_first_digit_numeral_list=numToWords(second_first_digits, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
                    complex_numeral.append((second_first_digit_numeral_list[0],second_first_digit_numeral_list[1],third_digit_numeral,second_first_digit_numeral_list[2]+1))
                else:
                    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,"singular",modifiers,agreement)
                    complex_numeral.append((third_digit_numeral,chosenNoun,0))

            elif (numbers_type == "cardinal"):
                if(second_first_digits>0):
                    third_digit_numeral=third_digit_numeral+" و "
                    second_first_digit_numeral_list=numToWords(second_first_digits, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
                    complex_numeral.append((third_digit_numeral,second_first_digit_numeral_list[0],second_first_digit_numeral_list[1],second_first_digit_numeral_list[2]+1))
                else:
                    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,"singular",modifiers,agreement)
                    complex_numeral.append((third_digit_numeral,chosenNoun,0))

        else:
            if numbers_type == "ordinal":
                complex_numeral.append(numToWords(int(digits), numerals[index], case,None,numbers_type,numerals[index]))
            else:
                complex_numeral.append(numToWords(int(digits), numerals[index], case,None,numbers_type))

    return complex_numeral



def numToWords(number, noun, case="nominative", gender = None, numbers_type = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    numberable_noun=""

    # Check number cateogry
    if(isinstance(number, int) and number >0 and number <3): # then Simplex - singular numeral
        numberable_noun=simplex_singular_numeral(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(number, int) and number >2 and number <=10): # then Simplex - added numeral
        numberable_noun=simplex_added_numeral(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(number, int) and number >10 and number <=12): # then compound - first subgroup numeral
        numberable_noun=compound_numeral_first_subgroup(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(number, int) and number >12 and number <=19): # then compound - second subgroup numeral
        numberable_noun=compound_numeral_second_subgroup(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(number, int) and number >19 and number <=99): # then complex - frist subgroup numeral
        numberable_noun=complex_numeral_first_subgroup(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(number, int) and number >99 and number <1000000000000): # then complex - second subgroup numeral
        numberable_noun=complex_numeral_second_subgroup(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)

        if((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly"):    #
            numberable_noun=complex_numeral_second_subgroup(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
        elif((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly"):    #
            numberable_noun=complex_numeral_second_subgroup(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)[0]

            if(numberable_noun[-1]==len(numberable_noun)-2):
                return str(number),numberable_noun[numberable_noun[-1]-1],0
            else:
                return str(number),numberable_noun[numberable_noun[-1]+1],0


    elif(isinstance(number, int) and number ==0 and noun not in numeral_names): # then Zero numeral
        chosenNoun = get_noun_dual_plural_gender(noun,case,gender,numbers_type,plural,"singular",modifiers,agreement)[0]
        if((isinstance(number_format, int) and number <= number_format) or number_format=="wordsOnly"):    #
            return zero_format,chosenNoun,0 # numeral, noun, numeral_index
        elif((isinstance(number_format, int) and number > number_format) or number_format=="digitsOnly"):    #
            return str(number),chosenNoun,0 # numeral, noun, numeral_index
        numberable_noun=complex_numeral_second_subgroup(number, noun, case, gender, numbers_type, plural, number_format, zero_format,modifiers,agreement)
    return numberable_noun


def ar_numToWords(number, case="nominative", gender = None, numbers_type = "cardinal", number_format = "wordsOnly", zero_format = "صفر"):
    # check params -------------------------------------------------------------------

    numbers_type=str(numbers_type).strip()
    if len(numbers_type)==0:
        numbers_type="cardinal"
    else:
        if (isinstance(numbers_type,str) and numbers_type.strip().lower() in ["cardinal","ordinal"]):
            numbers_type=numbers_type.strip().lower()
        else:
            return False,"Type value is not valid"


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
        return { 'error':True,'message':'number type not supported'}

    number_format=str(number_format).strip()
    try:
        number_format = int(number_format)
    except ValueError:
        if len(number_format) ==0:
            number_format= "wordsOnly"
        elif number_format != "wordsOnly" and number_format != "digitsOnly":
            return jsonify({ 'error':True, 'message':' Number Format field can take only one of these values (digitsOnly, wordsOnly or a number)'});

    zero_format=str(zero_format).strip()
    if len(zero_format) ==0:
        zero_format= "صفر"




    # end check params ----------------------------------------------------------------------------
    if isinstance(number,int):
        numberable_noun=numToWords(number,"",case,gender,numbers_type,None,number_format,zero_format)

        numberable_noun_printable=""
        if type(numberable_noun) is list:
            if(numbers_type=="cardinal"):
                numberable_noun.reverse()
            if(type(numberable_noun[0]) is tuple):
                numberable_noun_printable=numberable_noun_printable+ ' '.join(numberable_noun[0][0:-1])
            else:
                numberable_noun_printable=numberable_noun_printable+ ' '.join(numberable_noun[0][0][0:-1])

            for numeral in numberable_noun[1:]:

                if type(numeral) is tuple:
                    if len(numeral[numeral[-1]])>0:
                        seperator=" , "
                        if numbers_type == "ordinal" and len(numberable_noun_printable.strip())>1:
                            seperator=" بعد "
                        numberable_noun_printable=numberable_noun_printable+seperator+ ' '.join(numeral[0:-1])
                    else:
                        seperator=" "
                        if numbers_type == "ordinal" and len(numberable_noun_printable.strip())>1:
                            seperator=" بعد"
                        numberable_noun_printable=numberable_noun_printable+seperator+ ' '.join(numeral[0:-1])
                if type(numeral) is list:
                    if len(numeral[0][numeral[0][-1]])>0:
                        numberable_noun_printable=numberable_noun_printable+" و "+ ' '.join(numeral[0][0:-1])
                    else:
                        numberable_noun_printable=numberable_noun_printable+" "+ ' '.join(numeral[0][0:-1])

        elif type(numberable_noun) is tuple:
            numberable_noun_printable=numberable_noun[numberable_noun[-1]]
        else:
            return { 'error':True,'message':'not found'}
    else:
        return { 'error':True,'message':'type not supported'}
    numberable_noun_printable=numberable_noun_printable.strip()
    if len(numberable_noun_printable)>0:
        return { 'result':numberable_noun_printable, 'error':False, 'message':""}
    else:
        return { 'error':True,'message':'not found'}
