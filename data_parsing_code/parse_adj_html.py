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


def insert_verb_inflection(root=None,
                           m_singular_nominative=None,
                           m_singular_accusative=None,
                           m_singular_genitive=None,
                           m_dual_nominative=None,
                           m_dual_accusative=None,
                           m_dual_genitive=None,
                           m_plural_nominative=None,
                           m_plural_accusative=None,
                           m_plural_genitive=None,
                           f_singular_nominative=None,
                           f_singular_accusative=None,
                           f_singular_genitive=None,
                           f_dual_nominative=None,
                           f_dual_accusative=None,
                           f_dual_genitive=None,
                           f_plural_nominative=None,
                           f_plural_accusative=None,
                           f_plural_genitive=None):
    cur = mysql.cursor(dictionary=True)
    query=("INSERT INTO `modifiers_2`( `root`,"
           +" `m_singular_nominative`, `m_singular_accusative`, `m_singular_genitive`,"
           +" `m_dual_nominative`, `m_dual_accusative`, `m_dual_genitive`,"
           +" `m_plural_nominative`, `m_plural_accusative`, `m_plural_genitive`,"
           +" `f_singular_nominative`, `f_singular_accusative`, `f_singular_genitive`,"
           +" `f_dual_nominative`, `f_dual_accusative`, `f_dual_genitive`,"
           +" `f_plural_nominative`, `f_plural_accusative`, `f_plural_genitive`"
            +") VALUES ("
            +"%(root)s,"
            +"%(m_singular_nominative)s,"
            +"%(m_singular_accusative)s,"
            +"%(m_singular_genitive)s,"
            +"%(m_dual_nominative)s,"
            +"%(m_dual_accusative)s,"
            +"%(m_dual_genitive)s,"
            +"%(m_plural_nominative)s,"
            +"%(m_plural_accusative)s,"
            +"%(m_plural_genitive)s,"
            +"%(f_singular_nominative)s,"
            +"%(f_singular_accusative)s,"
            +"%(f_singular_genitive)s,"
            +"%(f_dual_nominative)s,"
            +"%(f_dual_accusative)s,"
            +"%(f_dual_genitive)s,"
            +"%(f_plural_nominative)s,"
            +"%(f_plural_accusative)s,"
            +"%(f_plural_genitive)s"
               ")")

    data = {
        'root':root ,
        'm_singular_nominative':m_singular_nominative ,
        'm_singular_accusative': m_singular_accusative,
        'm_singular_genitive': m_singular_genitive,
        'm_dual_nominative':m_dual_nominative ,
        'm_dual_accusative': m_dual_accusative,
        'm_dual_genitive': m_dual_genitive,
        'm_plural_nominative': m_plural_nominative,
        'm_plural_accusative': m_plural_accusative,
        'm_plural_genitive': m_plural_genitive,
        'f_singular_nominative':f_singular_nominative ,
        'f_singular_accusative': f_singular_accusative,
        'f_singular_genitive': f_singular_genitive,
        'f_dual_nominative':f_dual_nominative ,
        'f_dual_accusative': f_dual_accusative,
        'f_dual_genitive': f_dual_genitive,
        'f_plural_nominative': f_plural_nominative,
        'f_plural_accusative': f_plural_accusative,
        'f_plural_genitive': f_plural_genitive

    }
    cur.execute(query,data)
    return


mycursor.execute("SELECT * FROM `adjectives_root`")

adjective_root_rows = mycursor.fetchall()
error_ids=[]
for adjective_root_row in adjective_root_rows:
    print(str(adjective_root_row['id']))
    try:


        file_path="adjectives_tables/arabic_adj_"+str(adjective_root_row['id'])+".html"

        root=adjective_root_row['adjective_root']
        m_singular_nominative=None
        m_singular_accusative=None
        m_singular_genitive=None
        m_dual_nominative=None
        m_dual_accusative=None
        m_dual_genitive=None
        m_plural_nominative=None
        m_plural_accusative=None
        m_plural_genitive=None
        f_singular_nominative=None
        f_singular_accusative=None
        f_singular_genitive=None
        f_dual_nominative=None
        f_dual_accusative=None
        f_dual_genitive=None
        f_plural_nominative=None
        f_plural_accusative=None
        f_plural_genitive=None
        with codecs.open(file_path, "r", encoding="utf-8") as  f:
            dfs = pd.read_html(f.read())


            list_of_values=dfs[0].values
            section_name="Singular"
            for row in list_of_values:

                if row[0] in ["Singular","Dual","Plural"]:
                    section_name=row[0]
                elif row[0] in ["Nominative","Accusative","Genitive"]:

                    if section_name == "Singular" and row[0] == "Nominative":
                        m_singular_nominative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and   len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_singular_nominative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and   len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None
                    elif section_name == "Singular" and row[0] == "Accusative":

                        m_singular_accusative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_singular_accusative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None
                    elif section_name == "Singular" and row[0] == "Genitive":
                        m_singular_genitive= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_singular_genitive= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None

                    elif section_name == "Dual" and row[0] == "Nominative":
                        m_dual_nominative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_dual_nominative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None
                    elif section_name == "Dual" and row[0] == "Accusative":
                        m_dual_accusative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_dual_accusative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None
                    elif section_name == "Dual" and row[0] == "Genitive":
                        m_dual_genitive= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_dual_genitive= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None

                    elif section_name == "Plural" and row[0] == "Nominative":
                        m_plural_nominative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_plural_nominative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None
                    elif section_name == "Plural" and row[0] == "Accusative":
                        m_plural_accusative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_plural_accusative= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None
                    elif section_name == "Plural" and row[0] == "Genitive":
                        m_plural_genitive= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[1])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[1]))) >0 else  None
                        f_plural_genitive= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))[0] if len(re.findall(r'[\u0600-\u06FF]+', row[3])) >0 and  len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(row[3]))) >0 else  None


            """
            print(m_singular_nominative)
            print(m_singular_accusative)
            print(m_singular_genitive)

            print(m_dual_nominative)
            print(m_dual_accusative)
            print(m_dual_genitive)

            print(m_plural_nominative)
            print(m_plural_accusative)
            print(m_plural_genitive)

            print(f_singular_nominative)
            print(f_singular_accusative)
            print(f_singular_genitive)

            print(f_dual_nominative)
            print(f_dual_accusative)
            print(f_dual_genitive)

            print(f_plural_nominative)
            print(f_plural_accusative)
            print(f_plural_genitive)
            """
            if m_singular_nominative is None or m_singular_accusative is None or m_singular_genitive is None:
                continue


            insert_verb_inflection( root,
                               m_singular_nominative,
                               m_singular_accusative,
                               m_singular_genitive,
                               m_dual_nominative,
                               m_dual_accusative,
                               m_dual_genitive,
                               m_plural_nominative,
                               m_plural_accusative,
                               m_plural_genitive,
                               f_singular_nominative,
                               f_singular_accusative,
                               f_singular_genitive,
                               f_dual_nominative,
                               f_dual_accusative,
                               f_dual_genitive,
                               f_plural_nominative,
                               f_plural_accusative,
                               f_plural_genitive)


    except:
        error_ids.append(str(adjective_root_row['id']))
        print("error",str(adjective_root_row['id']))


mysql.commit()
print(error_ids)
