# -*- coding: utf-8 -*-
"""
Created on Mon May 25 19:49:37 2020

@author: Roaa
"""
import codecs
import pandas as pd
import numpy as np
import mysql.connector as MySQL
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
        #print(text)
        text = re.sub(arabic_diacritics, '', text)
    except:
        #print("error",text)
        return text
        
    return text

mysql = MySQL.connect(host='localhost',
                      database='ar_nlg'
                      , user='root'
                      , password='')
mycursor = mysql.cursor(dictionary=True)


def insert_verb_inflection(singular_a=None,
                           singular_n=None,
                           singular_g=None,
                           dual_a=None,
                           dual_n=None,
                           dual_g=None,
                           plural_a=None,
                           plural_n=None,
                           plural_g=None,
                           gender=None,
                           is_human=None):
    cur = mysql.cursor(dictionary=True)
    query=("INSERT INTO `nouns_2` ( `singular_a`, `singular_n`,`singular_g`,"
            +"`dual_a`, `dual_n`, "
            +"`dual_g`, `plural_a`, "
            +"`plural_n`, `plural_g`,`gender`, `is_human`"
            +") VALUES ("
            +"%(singular_a)s,"
            +"%(singular_n)s,"
            +"%(singular_g)s,"
            +"%(dual_a)s,"
            +"%(dual_n)s,"
            +"%(dual_g)s,"
            +"%(plural_a)s,"
            +"%(plural_n)s,"
            +"%(plural_g)s,"
            +"%(gender)s,"
            +"%(is_human)s"
               ")")

    data = {
        'singular_a':singular_a ,
        'singular_n':singular_n ,
        'singular_g':singular_g ,
        'dual_a': dual_a,
        'dual_n': dual_n,
        'dual_g': dual_g,
        'plural_a': plural_a,
        'plural_n': plural_n,
        'plural_g': plural_g,
        'gender': gender,
        'is_human': is_human

    }
    cur.execute(query,data)
    return


mycursor.execute("SELECT * FROM `nouns_root` ")

noun_root_rows = mycursor.fetchall()
error_ids=[]
for noun_root_row in noun_root_rows:
    print(str(noun_root_row['id']))
    try:
            
        
        file_path="nouns_tables/arabic_noun_"+str(noun_root_row['id'])+".html"
        gender=1
        singular_a=None
        singular_n=None
        singular_g=None
        dual_a=None
        dual_n=None
        dual_g=None
        plural_a=None
        plural_n=None
        plural_g=None
        is_human=1
        with codecs.open(file_path, "r", encoding="utf-8") as  f:
            dfs = pd.read_html(f.read())
            
            
            list_of_values=dfs[0].values
            section_name="Singular"
            for row in list_of_values:
                
                if row[0] in ["Singular","Dual","Plural"]:
                    section_name=row[0]
                elif row[0] in ["Nominative","Accusative","Genitive"]:

                    if section_name == "Singular" and row[0] == "Nominative":
                        singular_n= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and   len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                    elif section_name == "Singular" and row[0] == "Accusative":

                        singular_a= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                    elif section_name == "Singular" and row[0] == "Genitive":
                        singular_g= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        
                    elif section_name == "Dual" and row[0] == "Nominative":
                        dual_n= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                    elif section_name == "Dual" and row[0] == "Accusative":
                        dual_a= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                    elif section_name == "Dual" and row[0] == "Genitive":
                        dual_g= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        
                    elif section_name == "Plural" and row[0] == "Nominative":
                        plural_n= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                    elif section_name == "Plural" and row[0] == "Accusative":
                        plural_a= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                    elif section_name == "Plural" and row[0] == "Genitive":
                        plural_g= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        
                        
            """
            print(singular_a)
            print(singular_n)
            print(singular_g)
            
            print(dual_a)
            print(dual_n)
            print(dual_g)
            
            print(plural_a)
            print(plural_n)
            print(plural_g)
            """
            if singular_a is None or singular_g is None or singular_n is None:
                continue

            
            insert_verb_inflection( singular_a,
                               singular_n,
                               singular_g,
                               dual_a,
                               dual_n,
                               dual_g,
                               plural_a,
                               plural_g,
                               plural_g,
                               gender,
                               is_human)
            
    except:
        error_ids.append(str(noun_root_row['id']))
        print("error",str(noun_root_row['id']))
                

mysql.commit()
print(error_ids)
    
