import json
import codecs
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
    text = re.sub(arabic_diacritics, '', text)
    return text

import mysql.connector as MySQL
mysql = MySQL.connect(host='localhost',
                      database='ar_nlg'
                      , user='root'
                      , password='')

def insert_adj(root=None,
               m_singular=None,
               m_dual_nominative=None,
               m_dual_accusative=None,
               m_dual_genitive=None,
               m_plural_nominative=None,
               m_plural_accusative=None,
               m_plural_genitive=None,
               f_singular=None,
               f_dual_nominative=None,
               f_dual_accusative=None,
               f_dual_genitive=None,
               f_plural_nominative=None,
               f_plural_accusative=None,
               f_plural_genitive=None):

    cur = mysql.cursor(dictionary=True)
    query=("INSERT INTO `modifiers_2`"
           +"( `root`, `m_singular`, `m_dual_nominative`, `m_dual_accusative`,"
           +" `m_dual_genitive`, `m_plural_nominative`, `m_plural_accusative`,"
           +" `m_plural_genitive`, `f_singular`, `f_dual_nominative`, `f_dual_accusative`,"
           +" `f_dual_genitive`, `f_plural_nominative`, `f_plural_accusative`, `f_plural_genitive`)"
           +" VALUES ("
           +"%(root)s, %(m_singular)s, %(m_dual_nominative)s, %(m_dual_accusative)s,"
           +" %(m_dual_genitive)s, %(m_plural_nominative)s, %(m_plural_accusative)s,"
           +" %(m_plural_genitive)s, %(f_singular)s, %(f_dual_nominative)s, %(f_dual_accusative)s,"
           +" %(f_dual_genitive)s, %(f_plural_nominative)s, %(f_plural_accusative)s, %(f_plural_genitive)s"
           +")")
    data = {
      'root': root,
      'm_singular': m_singular,
      'm_dual_nominative': m_dual_nominative,
      'm_dual_accusative': m_dual_accusative,
      'm_dual_genitive': m_dual_genitive,
      'm_plural_nominative': m_plural_nominative,
      'm_plural_accusative': m_plural_accusative,
      'm_plural_genitive': m_plural_genitive,
      'f_singular': f_singular,
      'f_dual_nominative': f_dual_nominative,
      'f_dual_accusative': f_dual_accusative,
      'f_dual_genitive': f_dual_genitive,
      'f_plural_nominative': f_plural_nominative,
      'f_plural_accusative': f_plural_accusative,
      'f_plural_genitive': f_plural_genitive,
    }
    cur.execute(query,data)
    #result = cur.fetchone()
    return


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
        elif (number_form == "plural"):
            if (gender == 1 and case == "nominative"): # if masculine and nominative add suffix "ون" 
                adjective=adjective+"ون"
            elif(gender == 1 and case != "nominative"): # if masculine and not nominative then add the suffix "ين" 
                adjective = adjective +"ين"
            if (gender == 0): # if feminine and not ending with "ة" then add suffix "ات"
                adjective=adjective+"ات"
    return adjective 

def get_m_plurals(m_plural,m_singular):
    m_plural_nominative=None
    m_plural_accusative=None
    m_plural_genitive=None
    if m_plural in ["sp","smp"] :
                    
        m_plural_nominative=getManualAdjectiveForm(m_singular,"nominative",1,"plural")
        m_plural_accusative=getManualAdjectiveForm(m_singular,"accusative",1,"plural")
        m_plural_genitive=getManualAdjectiveForm(m_singular,"genitive",1,"plural")

    else:
        if  re.search('[a-zA-Z]',m_plural) and "/" in m_plural:
            
            pl_temp=remove_diacritics(m_plural)
            m_plural=pl_temp.split("/")[0]
        elif( re.search('[a-zA-Z]',m_plural) and "/" not in m_plural):
            return m_plural_nominative,m_plural_accusative,m_plural_genitive
        if(m_plural.endswith("ون")):
            # so it is sound plural
            m_plural_nominative=m_plural
            m_plural_accusative=m_plural[:-2]+"ين"
            m_plural_genitive=m_plural[:-2]+"ين"
        else:
            # then it is broken plural
            m_plural_nominative=m_plural
            m_plural_accusative=m_plural
            m_plural_genitive=m_plural
    return m_plural_nominative,m_plural_accusative,m_plural_genitive


template_name=["ar-adj-fem","ar-adj","ar-adj-pl","ar-adj-sound"]
    
with open("arabic_adjectives_v4.json", encoding='utf-8') as f1:
    lines = f1.readlines()
    count=0
    plural=0
    dual=0
    for i, line in enumerate(lines):
        json_line=str(line).strip()
        if(len(json_line)==1):
            continue
        elif(json_line[-1]==","):
            json_line=json_line[:-1]
        #print(json_line)
        json_data = json.loads(json_line)
        singualr=remove_diacritics(json_data["word"])
        root=None
        m_singular=None
        m_dual_nominative=None
        m_dual_accusative=None
        m_dual_genitive=None
        m_plural_nominative=None
        m_plural_accusative=None
        m_plural_genitive=None
        f_singular=None
        f_dual_nominative=None
        f_dual_accusative=None
        f_dual_genitive=None
        f_plural_nominative=None
        f_plural_accusative=None
        f_plural_genitive=None
        if "heads" in json_data:
            #print("in")
            json_head=json_data["heads"][0]
            #print(json_head)
            if(json_head["template_name"] not in template_name):
                #print(json_head["template_name"])
                plural=plural
            if (json_head["template_name"]=="ar-adj-fem"):
            
                f_singular=remove_diacritics(json_data["word"])
                
                #get masculine info if exist
                if("senses" in json_data and "inflection_of" in json_data["senses"][0] and not re.search('[a-zA-Z]', json_data["senses"][0]["inflection_of"][0])):
                    m_singular=remove_diacritics(json_data["senses"][0]["inflection_of"][0])
                    m_dual_nominative=getManualAdjectiveForm(m_singular,"nominative",1,"dual")
                    m_dual_accusative=getManualAdjectiveForm(m_singular,"accusative",1,"dual")
                    m_dual_genitive=getManualAdjectiveForm(m_singular,"genitive",1,"dual")
                elif f_singular.endswith('ة'):
                    m_singular=f_singular[:-1]
                    m_dual_nominative=getManualAdjectiveForm(m_singular,"nominative",1,"dual")
                    m_dual_accusative=getManualAdjectiveForm(m_singular,"accusative",1,"dual")
                    m_dual_genitive=getManualAdjectiveForm(m_singular,"genitive",1,"dual")
                
                #get feminine duals manually                
                f_dual_nominative=getManualAdjectiveForm(f_singular,"nominative",0,"dual")
                f_dual_accusative=getManualAdjectiveForm(f_singular,"accusative",0,"dual")
                f_dual_genitive=getManualAdjectiveForm(f_singular,"genitive",0,"dual")
                
                
                #get feminine plural if exist
    
                if("pl" in json_head and not re.search('[a-zA-Z]', json_head["pl"])):
                    f_plural_nominative=remove_diacritics(json_head["pl"])
                    f_plural_accusative=remove_diacritics(json_head["pl"])
                    f_plural_genitive=remove_diacritics(json_head["pl"])

                elif("conjugation" in json_data and "pl" in json_data["conjugation"][0] ):
                    if json_data["conjugation"][0]["pl"] in ["sp","sfp","smp"] :
                    
                        f_plural_nominative=getManualAdjectiveForm(f_singular,"nominative",0,"plural")
                        f_plural_accusative=getManualAdjectiveForm(f_singular,"accusative",0,"plural")
                        f_plural_genitive=getManualAdjectiveForm(f_singular,"genitive",0,"plural")

                    else:
                        f_plural=remove_diacritics(json_data["conjugation"][0]["pl"])
                        if  re.search('[a-zA-Z]',json_data["conjugation"][0]["pl"]) and "/" in json_data["conjugation"][0]["pl"]:
                            
                            pl_temp=remove_diacritics(json_data["conjugation"][0]["pl"])
                            f_plural=pl_temp.split("/")[0]
                        f_plural_nominative=f_plural
                        f_plural_accusative=f_plural
                        f_plural_genitive=f_plural
                """
                insert_adj(root,
                   m_singular,
                   m_dual_nominative,
                   m_dual_accusative,
                   m_dual_genitive,
                   m_plural_nominative,
                   m_plural_accusative,
                   m_plural_genitive,
                   f_singular,
                   f_dual_nominative,
                   f_dual_accusative,
                   f_dual_genitive,
                   f_plural_nominative,
                   f_plural_accusative,
                   f_plural_genitive)
                """
            elif (json_head["template_name"]=="ar-adj"):
                #get male singular and dual
                m_singular=remove_diacritics(json_data["word"])
                m_dual_nominative=getManualAdjectiveForm(m_singular,"nominative",1,"dual")
                m_dual_accusative=getManualAdjectiveForm(m_singular,"accusative",1,"dual")
                m_dual_genitive=getManualAdjectiveForm(m_singular,"genitive",1,"dual")
                
                # get female singular and dual
                if("f" in json_head and not re.search('[a-zA-Z]', json_head["f"])):
                    f_singular=remove_diacritics(json_head["f"])
                    f_dual_nominative=getManualAdjectiveForm(f_singular,"nominative",0,"dual")
                    f_dual_accusative=getManualAdjectiveForm(f_singular,"accusative",0,"dual")
                    f_dual_genitive=getManualAdjectiveForm(f_singular,"genitive",0,"dual")

                elif("conjugation" in json_data and "f" in json_data["conjugation"][0] ):
                    f_singular=remove_diacritics(json_data["conjugation"][0]["f"])
                    f_dual_nominative=getManualAdjectiveForm(f_singular,"nominative",0,"dual")
                    f_dual_accusative=getManualAdjectiveForm(f_singular,"accusative",0,"dual")
                    f_dual_genitive=getManualAdjectiveForm(f_singular,"genitive",0,"dual")
                    
                #get male plurals
                    
                if("Pl" in json_head ):
                    m_plural_nominative,m_plural_accusative,m_plural_genitive,=get_m_plurals(json_head["pl"],m_singular)

                elif("conjugation" in json_data and "pl" in json_data["conjugation"][0] ):
                    m_plural=remove_diacritics(json_data["conjugation"][0]["pl"])
                    m_plural_nominative,m_plural_accusative,m_plural_genitive,=get_m_plurals(m_plural,m_singular)
                elif("cPl" in json_head ):
                    m_plural=remove_diacritics(json_head["cpl"])
                    m_plural_nominative,m_plural_accusative,m_plural_genitive,=get_m_plurals(m_plural,m_singular)
                elif("conjugation" in json_data and "cpl" in json_data["conjugation"][0]):
                    m_plural=remove_diacritics(json_data["conjugation"][0]["cpl"])
                    m_plural_nominative,m_plural_accusative,m_plural_genitive,=get_m_plurals(m_plural,m_singular)
                    
                # get female plural
                
    
                if("fpl" in json_head and not re.search('[a-zA-Z]', json_head["fpl"])):
                    f_plural_nominative=remove_diacritics(json_head["fpl"])
                    f_plural_accusative=remove_diacritics(json_head["fpl"])
                    f_plural_genitive=remove_diacritics(json_head["fpl"])

                elif("conjugation" in json_data and "fpl" in json_data["conjugation"][0] ):
                    if json_data["conjugation"][0]["fpl"] in ["sp","sfp","smp"] and f_singular is not None:
                    
                        f_plural_nominative=getManualAdjectiveForm(f_singular,"nominative",0,"plural")
                        f_plural_accusative=getManualAdjectiveForm(f_singular,"accusative",0,"plural")
                        f_plural_genitive=getManualAdjectiveForm(f_singular,"genitive",0,"plural")

                    else:
                        f_plural=remove_diacritics(json_data["conjugation"][0]["fpl"])
                        if  re.search('[a-zA-Z]',json_data["conjugation"][0]["fpl"]) and "/" in json_data["conjugation"][0]["pl"]:
                            
                            pl_temp=remove_diacritics(json_data["conjugation"][0]["fpl"])
                            f_plural=pl_temp.split("/")[0]
                        if not re.search('[a-zA-Z]',f_plural):
                            f_plural_nominative=f_plural
                            f_plural_accusative=f_plural
                            f_plural_genitive=f_plural
                """
                insert_adj(root,
                   m_singular,
                   m_dual_nominative,
                   m_dual_accusative,
                   m_dual_genitive,
                   m_plural_nominative,
                   m_plural_accusative,
                   m_plural_genitive,
                   f_singular,
                   f_dual_nominative,
                   f_dual_accusative,
                   f_dual_genitive,
                   f_plural_nominative,
                   f_plural_accusative,
                   f_plural_genitive)
                """
            elif (json_head["template_name"]=="ar-adj-pl"):
                
                m_plural=remove_diacritics(json_data["word"])
                
                #get masculine info if exist
                if("senses" in json_data and "glosses" in json_data["senses"][0] ):# and not re.search('[a-zA-Z]', json_data["senses"][0]["inflection_of"][0])):
                    m_singular_raw=remove_diacritics(json_data["senses"][0]["glosses"][0])
                    if re.search('[a-zA-Z]', m_singular_raw) and '"' in m_singular_raw:
                        m_singular=m_singular_raw.split('"')[1]
                        
                        m_dual_nominative=getManualAdjectiveForm(m_singular,"nominative",1,"dual")
                        m_dual_accusative=getManualAdjectiveForm(m_singular,"accusative",1,"dual")
                        m_dual_genitive=getManualAdjectiveForm(m_singular,"genitive",1,"dual")
                        
                        m_plural_nominative,m_plural_accusative,m_plural_genitive,=get_m_plurals(m_plural,m_singular)
                        """
                        insert_adj(root,
                           m_singular,
                           m_dual_nominative,
                           m_dual_accusative,
                           m_dual_genitive,
                           m_plural_nominative,
                           m_plural_accusative,
                           m_plural_genitive,
                           f_singular,
                           f_dual_nominative,
                           f_dual_accusative,
                           f_dual_genitive,
                           f_plural_nominative,
                           f_plural_accusative,
                           f_plural_genitive)
                        """
            elif (json_head["template_name"]=="ar-adj-sound"):
                count+=1
                m_singular=remove_diacritics(json_data["word"])
                m_dual_nominative=getManualAdjectiveForm(m_singular,"nominative",1,"dual")
                m_dual_accusative=getManualAdjectiveForm(m_singular,"accusative",1,"dual")
                m_dual_genitive=getManualAdjectiveForm(m_singular,"genitive",1,"dual")
                m_plural_nominative=getManualAdjectiveForm(m_singular,"nominative",1,"plural")
                m_plural_accusative=getManualAdjectiveForm(m_singular,"accusative",1,"plural")
                m_plural_genitive=getManualAdjectiveForm(m_singular,"genitive",1,"plural")
                
                
                f_singular=remove_diacritics(m_singular+"ة")
                f_dual_nominative=getManualAdjectiveForm(f_singular,"nominative",0,"dual")
                f_dual_accusative=getManualAdjectiveForm(f_singular,"accusative",0,"dual")
                f_dual_genitive=getManualAdjectiveForm(f_singular,"genitive",0,"dual")
                f_plural_nominative=getManualAdjectiveForm(f_singular,"nominative",0,"plural")
                f_plural_accusative=getManualAdjectiveForm(f_singular,"accusative",0,"plural")
                f_plural_genitive=getManualAdjectiveForm(f_singular,"genitive",0,"plural")
                
                """
                insert_adj(root,
                   m_singular,
                   m_dual_nominative,
                   m_dual_accusative,
                   m_dual_genitive,
                   m_plural_nominative,
                   m_plural_accusative,
                   m_plural_genitive,
                   f_singular,
                   f_dual_nominative,
                   f_dual_accusative,
                   f_dual_genitive,
                   f_plural_nominative,
                   f_plural_accusative,
                   f_plural_genitive)
                """
                
                        
                        
              
       
    mysql.commit()
    
    print(count,plural,dual)
                    
            


