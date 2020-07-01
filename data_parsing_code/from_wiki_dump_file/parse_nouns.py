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

def insert_noun(singular,gender=None,dual_a=None,dual_n=None,dual_g=None, plural_a=None, plural_n=None,plural_g=None,is_human=None):

    cur = mysql.cursor(dictionary=True)
    query=("INSERT INTO `nouns_2`(`singular`, `gender`, `dual_a`, `dual_n`, `dual_g`, `plural_a`, `plural_n`, `plural_g`, `is_human`) VALUES ("
                     +"%(singular)s, %(gender)s, %(dual_a)s, %(dual_n)s, %(dual_g)s, %(plural_a)s, %(plural_n)s, %(plural_g)s, %(is_human)s"
                     +")")
    data = {
      'singular': singular,
      'gender': gender,
      'dual_a': dual_a,
      'dual_n': dual_n,
      'dual_g': dual_g,
      'plural_a': plural_a,
      'plural_n': plural_n,
      'plural_g': plural_g,
      'is_human': is_human,
    }
    cur.execute(query,data)
    #result = cur.fetchone()
    return

template_name=["ar-adj","ar-noun-inf-cons","ar-noun","head","ar-noun-dual","ar-noun-pl","ar-noun-nisba","ar-noun-form"]
    
with open("arabic_results_noun_v4.json", encoding='utf-8') as f1:
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
        gender=None
        dual_a=None
        dual_n=None
        dual_g=None
        plural_a=None
        plural_n=None
        plural_g=None
        is_human=True
        if "heads" in json_data:
            #print("in")
            json_head=json_data["heads"][0]
            #print(json_head)
            
            if( json_head["template_name"] == "ar-noun"):
                if("2" in json_head and json_head["2"] in ["m","f"]):
                    gender=False
                    if(json_head["2"]=="m"):
                        gender=True
                    if("pl" in json_head and not re.search('[a-zA-Z]', json_head["pl"])):
                        plural_n=remove_diacritics(json_head["pl"])
                    if ("d" in json_head and not re.search('[a-zA-Z]', json_head["d"])):
                        dual_n=remove_diacritics(json_head["d"])
                    if ("f" in json_head and "fpl" in json_data["conjugation"][0] and not re.search('[a-zA-Z]', json_data["conjugation"][0]["fpl"])):
                        #insert_noun(singular=remove_diacritics(json_head["f"]),gender=False,plural_n=remove_diacritics(json_data["conjugation"][0]["fpl"]),is_human=is_human)
                        plural+=1
                    
                    #insert_noun(singular=singualr,gender=gender,dual_a=dual_a,dual_n=dual_n,dual_g=dual_g, plural_a=plural_a, plural_n=plural_n,plural_g=plural_g,is_human=is_human)
                else:
                    with codecs.open("arabic_nouns_not_f_m.json", "a", encoding="utf-8") as f2:
                        
                        data = json.dumps(json_data, ensure_ascii = False)
                        #f2.write(data+"\n")
            elif( json_head["template_name"] == "ar-noun-pl"):
                if("senses" in json_data and "inflection_of" in json_data["senses"][0] and not re.search('[a-zA-Z]', json_data["senses"][0]["inflection_of"][0])):
                    if("2" in json_head and json_head["2"] == "f-p"):
                        gender=False
                    elif ("2" in json_head and json_head["2"] == "m-p"):
                        gender=True
                    insert_noun(singular=remove_diacritics(json_data["senses"][0]["inflection_of"][0]),gender=gender,dual_a=dual_a,dual_n=dual_n,dual_g=dual_g, plural_a=plural_a, plural_n=singualr,plural_g=plural_g,is_human=is_human)
                    
                count+=1
            

    mysql.commit()
    print(count,plural,dual)
                    
            


