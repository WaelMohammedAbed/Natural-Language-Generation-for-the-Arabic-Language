import mysql.connector as MySQL
from numeral_names import numeral_names
import yaml



# Configure db
db = yaml.safe_load(open('db.yaml'))

mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])

def get_noun_dual_plural_gender(noun,case="nominative",gender = None,dual=None,plural=None,chosen_type="singular",modifiers=[],agreement=True):
    pluralByCase={'accusative': "plural_a", 'nominative': "plural_n", 'genitive':"plural_g"}
    dualByCase={'accusative': "dual_a", 'nominative': "dual_n", 'genitive':"dual_g"}
    cur = mysql.cursor(buffered=True,dictionary=True)
    select_singular=("SELECT * FROM `nouns` WHERE "
                     +"`singular` = %(noun)s "
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
        if (nounDetails == None or (nounDetails != None and nounDetails["singular"] == None)):
            chosenNoun=noun
        else:
            chosenNoun=nounDetails["singular"]
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

    # check if noun is for human or not
    is_human=None
    if(nounDetails != None and nounDetails["is_human"] != None):
        is_human=nounDetails["is_human"]
    #set modifiers if exist
    modifiers=get_noun_modifiers(modifiers,case,gender,chosen_type,is_human,agreement)
    
    modifiers_text=""
    for modifier in modifiers:
        modifiers_text+=" "+modifier+" و"
    if len(modifiers_text)>0: #remove  و
        modifiers_text=modifiers_text[0:-1]
        chosenNoun+=modifiers_text
    #print(modifiers_text,modifiers)

    return chosenNoun,gender #dual,plural,gender,is_human


def getManualAdjectiveForm(adjective,case,gender,number_form):
    
    # most of the feminine adj ends with "ة", therefore it will treated as feminine sound plural
    if adjective.endswith('ة') or adjective.endswith('ه'):
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
        if( number_form == "singular"):
            return adjective
        elif (number_form =="dual"):
            if (gender == 1 and case == "nominative"): # if masculine and nominative add suffix "ان" 
                adjective=adjective+"ان"
            elif(gender == 1 and case != "nominative"): # if masculine and not nominative then add the suffix "ين" 
                adjective = adjective +"ين"
            elif (gender == 0 and case == "nominative"): # if masculine and nominative add suffix "ان" 
                return adjective+"تان"
            elif(gender == 0 and case != "nominative"): # if masculine and not nominative then add the suffix "ين" 
                return adjective+"تين"
        else:
            if (gender == 1 and case == "nominative"): # if masculine and nominative add suffix "ون" 
                adjective=adjective+"ون"
            elif(gender == 1 and case != "nominative"): # if masculine and not nominative then add the suffix "ين" 
                adjective = adjective +"ين"
            if (gender == 0): # if feminine and not ending with "ة" then add suffix "ات"
                adjective=adjective+"ات"
    return adjective 
def get_noun_modifiers(modifiers,
                        case="nominative",
                        gender=True,
                        number_form = "singular",
                        is_human=True,
                        agreement=True):
    column="f_"
    if gender:
        column="m_"
    if number_form == "singular":# if singular case is neglected
        column=column+number_form
    else:
        column=column+number_form+"_"+case
    
    inflected_modifiers=[]
    for adjective in modifiers:
        select_adjective=("SELECT * FROM `modifiers` WHERE "
                          +"`root` = %(root)s OR " 
                          +"`m_singular` = %(m_singular)s OR "
                          +"`m_dual_nominative` = %(m_dual_nominative)s OR "
                          +"`m_dual_accusative` = %(m_dual_accusative)s OR "
                          +"`m_dual_genitive`  = %(m_dual_genitive)s OR "
                          +"`m_plural_nominative` = %(m_plural_nominative)s OR "
                          +"`m_plural_accusative`  = %(m_plural_accusative)s OR "
                          +"`m_plural_genitive`  = %(m_plural_genitive)s OR "
                          +"`f_singular`  = %(f_singular)s OR "
                          +"`f_dual_nominative` = %(f_dual_nominative)s OR "
                          +"`f_dual_accusative`  = %(f_dual_accusative)s OR "
                          +"`f_dual_genitive` = %(f_dual_genitive)s OR "
                          +"`f_plural_nominative` = %(f_plural_nominative)s OR "
                          +"`f_plural_accusative` = %(f_plural_accusative)s OR "
                          +"`f_plural_genitive` = %(f_plural_genitive)s ")
        data_adjective = {
            'root': adjective,
            'm_singular': adjective,
            'm_dual_nominative': adjective,
            'm_dual_accusative': adjective,
            'm_dual_genitive': adjective,
            'm_plural_nominative': adjective,
            'm_plural_accusative': adjective,
            'm_plural_genitive': adjective,
            'f_singular': adjective,
            'f_dual_nominative': adjective,
            'f_dual_accusative': adjective,
            'f_dual_genitive': adjective,
            'f_dual_genitive': adjective,
            'f_plural_nominative': adjective,
            'f_plural_accusative': adjective,
            'f_plural_genitive': adjective,
        }
        cur = mysql.cursor(buffered=True,dictionary=True)
        cur.execute(select_adjective,data_adjective)
        adjectiveDetails = cur.fetchone()
        # deflected agreement condition
        if not is_human and not agreement and number_form== 'plural':
            #condition is true then take the feminine singular form
            column="f_singular"
            
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
            
    

def get_numeral(count,case,gender):
    select_numeral=("SELECT `numeral` FROM `numerals` WHERE `number` = %(number)s AND  `gender` = %(gender)s AND `noun_case` = %(noun_case)s")
    data_numeral = {
      'number': count,
      'noun_case': case,
      'gender': gender,
    }
    cur = mysql.cursor(buffered=True)
    cur.execute(select_numeral,data_numeral)
    numeralDetails = cur.fetchone()
    return numeralDetails[0]



def simplex_singular_numeral(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    chosen_type="singular"
    if(count==2):
        chosen_type="dual"
        
    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,dual,plural,chosen_type,modifiers,agreement)
    numeral=get_numeral(count,case,gender)
    numeralNumber=2
    
    if(noun in numeral_names):
        numeral=""
        numeralNumber=""
    if(count ==1 and ((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly")):    #
        return chosenNoun,numeral,1 # noun, numeral, numeral_index
    elif(count ==1 and ((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly")):    #
        return chosenNoun+"1",1 # noun, numeral, numeral_index
    elif(count ==2 and ((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly")):    #
        return chosenNoun,numeral,1 # noun, numeral, numeral_index
    elif(count ==2 and ((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly")):    #
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
    
def simplex_added_numeral(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,dual,plural,"plural",modifiers,agreement)
    
    gender = 1 - gender # toggle the gender as the numeral takes the opposite gender of the noun in added numeral group
    
    
    numeralDetails=get_numeral(count,case,gender)
    if(count >2 and count <=10 and ((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly")):    #
        return numeralDetails,chosenNoun,0 # numeral, noun, numeral_index
    elif(count >2 and count <=10 and ((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly")):    #
        return str(count),chosenNoun,0 # numeral, noun, numeral_index
    else:
        return "error"
        
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

# Group Compound nouns
def compound_numeral_first_subgroup(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    
    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,dual,plural,"singular",modifiers,agreement)
    
    
        
    numeralDetails=get_numeral(count,case,gender)
    if(count >10 and count <=12 and ((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly")):    #
        return numeralDetails,chosenNoun,0 # numeral, noun, numeral_index
    elif(count >10 and count <=12 and ((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly")):    #
        return str(count),chosenNoun,0 # numeral, noun, numeral_index
    else:
        return "error"


def compound_numeral_second_subgroup(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    
    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,dual,plural,"singular",modifiers,agreement)
        
    numeralDetails=get_numeral(10,case,gender)
    
    gender=1-gender
    
    unit=count%10
    
    unitNumeralDetails=get_numeral(unit,case,gender)
    

    

    if(count >12 and count <=19 and ((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly")):    #
        return unitNumeralDetails+" "+numeralDetails,chosenNoun,0 # numeral, noun, numeral_index
    elif(count >12 and count <=19 and ((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly")):    #
        return str(count),chosenNoun,0 # numeral, noun, numeral_index
    else:
        return "error"
    
def complex_numeral_first_subgroup(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    
    digits=[int(x) for x in str(count)]
    units=digits[1]
    units_numeral=""
    if(int(units)>0):
        unitsDetails=countable2(units, noun, case, gender, dual, plural, number_format, zero_format)
        units_numeral=unitsDetails[unitsDetails[2]]+" و "
    tens=digits[0]
    
    
    if(tens==2):
        tens=(tens-1)*10
        
    
    tensDetails=countable2(tens, "", "nominative", 0)
    tens_numeral=getManualNounPlural(tensDetails[tensDetails[2]],case,1)
    
    chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,dual,plural,"singular",modifiers,agreement)
        
   

    if(count >19 and count <=99 and ((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly")):    #
        return units_numeral+tens_numeral,chosenNoun,0 # numeral, noun, numeral_index
    elif(count >19 and count <=99 and ((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly")):    #
        return str(count),chosenNoun,0 # numeral, noun, numeral_index
    else:
        return "error"
    
def complex_numeral_second_subgroup(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    threeDigits=[]
    threeDigits.append(str(count)[-3:])
    for i in range(3, len(str(count)), 3):
        threeDigits.append(str(count)[-3-i:-i])
    numerals=numeral_names
    complex_numeral=[]
    for index,digits in enumerate(threeDigits):
        if(index==0):
            thrid_digit_numeral=""
            thrid_digit_numeral_list=[]
            if(len(digits)==3 and int(digits[0])==1):
                thrid_digit_numeral=numerals[0]
            elif(len(digits)==3 and int(digits[0])==2):
                thrid_digit_numeral=get_noun_dual_plural_gender(numerals[0],case,0,None,None,"dual")[0]
            elif(len(digits)==3 and int(digits[0])>2):
                thrid_digit_numeral_list=countable2(int(digits[0]), numerals[0], case, gender, dual, numerals[0], number_format, zero_format)
                
                thrid_digit_numeral=thrid_digit_numeral_list[0]+" "+thrid_digit_numeral_list[1]
            
            second_first_digits=int(digits[1]+digits[2])
            second_first_digit_numeral_list=["","",""]
            if(second_first_digits>0):
                thrid_digit_numeral=thrid_digit_numeral+" و "
                second_first_digit_numeral_list=countable2(second_first_digits, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
                complex_numeral.append((thrid_digit_numeral,second_first_digit_numeral_list[0],second_first_digit_numeral_list[1],second_first_digit_numeral_list[2]+1))
            else:
                chosenNoun,gender=get_noun_dual_plural_gender(noun,case,gender,dual,plural,"singular",modifiers,agreement)
                complex_numeral.append((thrid_digit_numeral,chosenNoun,0))
            
        else:
            complex_numeral.append(countable2(int(digits), numerals[index], case))
            
    return complex_numeral
        


def countable2(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر",modifiers=[],agreement=True):
    countable_noun=""
    
    # Check count cateogry
    if(isinstance(count, int) and count >0 and count <3): # then Simplex - singular numeral
        countable_noun=simplex_singular_numeral(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(count, int) and count >2 and count <=10): # then Simplex - added numeral
        countable_noun=simplex_added_numeral(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(count, int) and count >10 and count <=12): # then compound - first subgroup numeral
        countable_noun=compound_numeral_first_subgroup(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(count, int) and count >12 and count <=19): # then compound - second subgroup numeral
        countable_noun=compound_numeral_second_subgroup(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(count, int) and count >19 and count <=99): # then complex - frist subgroup numeral
        countable_noun=complex_numeral_first_subgroup(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
    elif(isinstance(count, int) and count >99 and count <1000000000000): # then complex - second subgroup numeral
        countable_noun=complex_numeral_second_subgroup(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
        
        if((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly"):    #
            countable_noun=complex_numeral_second_subgroup(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
        elif((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly"):    #
            countable_noun=complex_numeral_second_subgroup(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)[0]
            print(countable_noun)
            if(countable_noun[-1]==len(countable_noun)-2):
                return str(count),countable_noun[countable_noun[-1]-1],0
            else:
                return str(count),countable_noun[countable_noun[-1]+1],0
                
        
    elif(isinstance(count, int) and count ==0 and noun not in numeral_names): # then Zero numeral
        chosenNoun = get_noun_dual_plural_gender(noun,case,gender,dual,plural,"singular",modifiers,agreement)[0]
        if((isinstance(number_format, int) and count <= number_format) or number_format=="wordsOnly"):    #
            return zero_format,chosenNoun,0 # numeral, noun, numeral_index
        elif((isinstance(number_format, int) and count > number_format) or number_format=="digitsOnly"):    #
            return str(count),chosenNoun,0 # numeral, noun, numeral_index
        countable_noun=complex_numeral_second_subgroup(count, noun, case, gender, dual, plural, number_format, zero_format,modifiers,agreement)
    return countable_noun


def countable(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر", modifiers=[], agreement= True):
    if isinstance(count,str) and (count=="dual" or count=="plural"):
        countable_noun_printable = get_noun_dual_plural_gender(noun,case,gender,dual,plural,count,modifiers,agreement)
    elif isinstance(count,int):
        countable_noun=countable2(count,noun,case,gender,dual,plural,number_format,zero_format,modifiers,agreement)
        
        countable_noun_printable=""
        if type(countable_noun) is list:
            countable_noun.reverse()
            if(type(countable_noun[0]) is tuple):
                countable_noun_printable=countable_noun_printable+ ' '.join(countable_noun[0][0:-1])
            else:
                countable_noun_printable=countable_noun_printable+ ' '.join(countable_noun[0][0][0:-1])
            
            for numeral in countable_noun[1:]:
                if type(numeral) is tuple:
                    if len(numeral[numeral[-1]])>0:
                        countable_noun_printable=countable_noun_printable+" و "+ ' '.join(numeral[0:-1])
                    else:
                        countable_noun_printable=countable_noun_printable+" "+ ' '.join(numeral[0:-1])
                if type(numeral) is list:
                    if len(numeral[0][numeral[0][-1]])>0:
                        countable_noun_printable=countable_noun_printable+" و "+ ' '.join(numeral[0][0:-1])
                    else:
                        countable_noun_printable=countable_noun_printable+" "+ ' '.join(numeral[0][0:-1])
                        
        elif type(countable_noun) is tuple:
            countable_noun_printable=' '.join(countable_noun[0:-1])
        else:
            return { 'error':True,'message':'not found'}
    else:
        return { 'error':True,'message':'type not supported'}
    
    if len(countable_noun_printable)>0:
        return { 'result':countable_noun_printable, 'error':False, 'message':""}
    else:
        return { 'error':'not found'}
    
    
