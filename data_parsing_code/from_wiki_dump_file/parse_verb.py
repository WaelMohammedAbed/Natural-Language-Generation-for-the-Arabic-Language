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

def insert_verb(verb_root=None,
               form_number=None):

    cur = mysql.cursor(dictionary=True)
    query=(" INSERT INTO `verbs`( `verb_root`, `form_number`) VALUES ("
           +"%(verb_root)s, %(form_number)s"
           +")")
    data = {
      'verb_root': verb_root,
      'form_number': form_number,

    }
    cur.execute(query,data)
    #result = cur.fetchone()
    return



template_name=["ar-verb","ar-verb-form"]
verb_forms=["I","II","III","IV","V","VI","VII","VIII","IX","X","Iq","IIq","XI","XII","XIII","XIV","XV","IIIq","IVq"]
    
with open("arabic_verbs_v4.json", encoding='utf-8') as f1:
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
        verb_root=None
        form_number=None
        if "heads" in json_data:
            #print("in")
            json_head=json_data["heads"][0]
            #print(json_head)
            if(json_head["template_name"] not in template_name):
                print(json_head["template_name"])
                
            if (json_head["template_name"]=="ar-verb"):
                verb_root=remove_diacritics(json_data["word"])
                if ("1" in json_head and json_head["1"] not in verb_forms):
                    if "sound" in json_head["1"]:
                        form_number=json_head["1"].split('-')[0]
                        insert_verb(verb_root,form_number)
                    count+=1
                    print(form_number)
                else:
                    form_number=json_head["1"]
                    insert_verb(verb_root,form_number)
                
            
            elif (json_head["template_name"]=="ar-verb-form"):
                if ("2" in json_head and json_head["2"] not in verb_forms):
                    plural+=1
                
            
                
            
               
                

    mysql.commit()
    
    print(count,plural,dual)
                    
            


