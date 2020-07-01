
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


def insert_verb_inflection(verb_root=None,
                           active_past_singular_1_m=None,
                           active_past_singular_1_f=None,
                           active_past_singular_2_m=None,
                           active_past_singular_2_f=None,
                           active_past_singular_3_m=None,
                           active_past_singular_3_f=None,
                           active_past_dual_2_m=None,
                           active_past_dual_2_f=None,
                           active_past_dual_3_m=None,
                           active_past_dual_3_f=None,
                           active_past_plural_1_m=None,
                           active_past_plural_1_f=None,
                           active_past_plural_2_m=None,
                           active_past_plural_2_f=None,
                           active_past_plural_3_m=None,
                           active_past_plural_3_f=None,
                           active_none_past_singular_1_m=None,
                           active_none_past_singular_1_f=None,
                           active_none_past_singular_2_m=None,
                           active_none_past_singular_2_f=None,
                           active_none_past_singular_3_m=None,
                           active_none_past_singular_3_f=None,
                           active_none_past_dual_2_m=None,
                           active_none_past_dual_2_f=None,
                           active_none_past_dual_3_m=None,
                           active_none_past_dual_3_f=None,
                           active_none_past_plural_1_m=None,
                           active_none_past_plural_1_f=None,
                           active_none_past_plural_2_m=None,
                           active_none_past_plural_2_f=None,
                           active_none_past_plural_3_m=None,
                           active_none_past_plural_3_f=None,
                           active_subjunctive_singular_1_m=None,
                           active_subjunctive_singular_1_f=None,
                           active_subjunctive_singular_2_m=None,
                           active_subjunctive_singular_2_f=None,
                           active_subjunctive_singular_3_m=None,
                           active_subjunctive_singular_3_f=None,
                           active_subjunctive_dual_2_m=None,
                           active_subjunctive_dual_2_f=None,
                           active_subjunctive_dual_3_m=None,
                           active_subjunctive_dual_3_f=None,
                           active_subjunctive_plural_1_m=None,
                           active_subjunctive_plural_1_f=None,
                           active_subjunctive_plural_2_m=None,
                           active_subjunctive_plural_2_f=None,
                           active_subjunctive_plural_3_m=None,
                           active_subjunctive_plural_3_f=None,
                           active_jussive_singular_1_m=None,
                           active_jussive_singular_1_f=None,
                           active_jussive_singular_2_m=None,
                           active_jussive_singular_2_f=None,
                           active_jussive_singular_3_m=None,
                           active_jussive_singular_3_f=None,
                           active_jussive_dual_2_m=None,
                           active_jussive_dual_2_f=None,
                           active_jussive_dual_3_m=None,
                           active_jussive_dual_3_f=None,
                           active_jussive_plural_1_m=None,
                           active_jussive_plural_1_f=None,
                           active_jussive_plural_2_m=None,
                           active_jussive_plural_2_f=None,
                           active_jussive_plural_3_m=None,
                           active_jussive_plural_3_f=None,
                           active_imperative_singular_2_m=None,
                           active_imperative_singular_2_f=None,
                           active_imperative_dual_2_m=None,
                           active_imperative_dual_2_f=None,
                           active_imperative_plural_2_m=None,
                           active_imperative_plural_2_f=None,

                           passive_past_singular_1_m=None,
                           passive_past_singular_1_f=None,
                           passive_past_singular_2_m=None,
                           passive_past_singular_2_f=None,
                           passive_past_singular_3_m=None,
                           passive_past_singular_3_f=None,
                           passive_past_dual_2_m=None,
                           passive_past_dual_2_f=None,
                           passive_past_dual_3_m=None,
                           passive_past_dual_3_f=None,
                           passive_past_plural_1_m=None,
                           passive_past_plural_1_f=None,
                           passive_past_plural_2_m=None,
                           passive_past_plural_2_f=None,
                           passive_past_plural_3_m=None,
                           passive_past_plural_3_f=None,
                           passive_none_past_singular_1_m=None,
                           passive_none_past_singular_1_f=None,
                           passive_none_past_singular_2_m=None,
                           passive_none_past_singular_2_f=None,
                           passive_none_past_singular_3_m=None,
                           passive_none_past_singular_3_f=None,
                           passive_none_past_dual_2_m=None,
                           passive_none_past_dual_2_f=None,
                           passive_none_past_dual_3_m=None,
                           passive_none_past_dual_3_f=None,
                           passive_none_past_plural_1_m=None,
                           passive_none_past_plural_1_f=None,
                           passive_none_past_plural_2_m=None,
                           passive_none_past_plural_2_f=None,
                           passive_none_past_plural_3_m=None,
                           passive_none_past_plural_3_f=None,
                           passive_subjunctive_singular_1_m=None,
                           passive_subjunctive_singular_1_f=None,
                           passive_subjunctive_singular_2_m=None,
                           passive_subjunctive_singular_2_f=None,
                           passive_subjunctive_singular_3_m=None,
                           passive_subjunctive_singular_3_f=None,
                           passive_subjunctive_dual_2_m=None,
                           passive_subjunctive_dual_2_f=None,
                           passive_subjunctive_dual_3_m=None,
                           passive_subjunctive_dual_3_f=None,
                           passive_subjunctive_plural_1_m=None,
                           passive_subjunctive_plural_1_f=None,
                           passive_subjunctive_plural_2_m=None,
                           passive_subjunctive_plural_2_f=None,
                           passive_subjunctive_plural_3_m=None,
                           passive_subjunctive_plural_3_f=None,
                           passive_jussive_singular_1_m=None,
                           passive_jussive_singular_1_f=None,
                           passive_jussive_singular_2_m=None,
                           passive_jussive_singular_2_f=None,
                           passive_jussive_singular_3_m=None,
                           passive_jussive_singular_3_f=None,
                           passive_jussive_dual_2_m=None,
                           passive_jussive_dual_2_f=None,
                           passive_jussive_dual_3_m=None,
                           passive_jussive_dual_3_f=None,
                           passive_jussive_plural_1_m=None,
                           passive_jussive_plural_1_f=None,
                           passive_jussive_plural_2_m=None,
                           passive_jussive_plural_2_f=None,
                           passive_jussive_plural_3_m=None,
                           passive_jussive_plural_3_f=None):
    cur = mysql.cursor(dictionary=True)
    query=("INSERT INTO `verbs_inflections`( `verb_root`, "
            +"`active_past_singular_1_m`, `active_past_singular_1_f`, "
            +"`active_past_singular_2_m`, `active_past_singular_2_f`, "
            +"`active_past_singular_3_m`, `active_past_singular_3_f`, "
            +"`active_past_dual_2_m`, `active_past_dual_2_f`, `active_past_dual_3_m`, "
            +"`active_past_dual_3_f`, `active_past_plural_1_m`, `active_past_plural_1_f`,"
            +"`active_past_plural_2_m`, `active_past_plural_2_f`, `active_past_plural_3_m`,"
            +"`active_past_plural_3_f`, `active_none_past_singular_1_m`,"
            +"`active_none_past_singular_1_f`, `active_none_past_singular_2_m`,"
            +"`active_none_past_singular_2_f`, `active_none_past_singular_3_m`,"
            +"`active_none_past_singular_3_f`, `active_none_past_dual_2_m`, "
            +"`active_none_past_dual_2_f`, `active_none_past_dual_3_m`, "
            +"`active_none_past_dual_3_f`, `active_none_past_plural_1_m`, "
            +"`active_none_past_plural_1_f`, `active_none_past_plural_2_m`, "
            +"`active_none_past_plural_2_f`, `active_none_past_plural_3_m`, "
            +"`active_none_past_plural_3_f`, `active_subjunctive_singular_1_m`, "
            +"`active_subjunctive_singular_1_f`, `active_subjunctive_singular_2_m`, "
            +"`active_subjunctive_singular_2_f`, `active_subjunctive_singular_3_m`, "
            +"`active_subjunctive_singular_3_f`, `active_subjunctive_dual_2_m`, "
            +"`active_subjunctive_dual_2_f`, `active_subjunctive_dual_3_m`, "
            +"`active_subjunctive_dual_3_f`, `active_subjunctive_plural_1_m`, "
            +"`active_subjunctive_plural_1_f`, `active_subjunctive_plural_2_m`, "
            +"`active_subjunctive_plural_2_f`, `active_subjunctive_plural_3_m`, "
            +"`active_subjunctive_plural_3_f`, `active_jussive_singular_1_m`, "
            +"`active_jussive_singular_1_f`, `active_jussive_singular_2_m`, "
            +"`active_jussive_singular_2_f`, `active_jussive_singular_3_m`, "
            +"`active_jussive_singular_3_f`, `active_jussive_dual_2_m`, "
            +"`active_jussive_dual_2_f`, `active_jussive_dual_3_m`, "
            +"`active_jussive_dual_3_f`, `active_jussive_plural_1_m`, "
            +"`active_jussive_plural_1_f`, `active_jussive_plural_2_m`, "
            +"`active_jussive_plural_2_f`, `active_jussive_plural_3_m`, "
            +"`active_jussive_plural_3_f`, `active_imperative_singular_2_m`, "
            +"`active_imperative_singular_2_f`, `active_imperative_dual_2_m`, "
            +"`active_imperative_dual_2_f`, `active_imperative_plural_2_m`, "
            +"`active_imperative_plural_2_f`, `passive_past_singular_1_m`,"
            +"`passive_past_singular_1_f`, `passive_past_singular_2_m`,"
            +"`passive_past_singular_2_f`, `passive_past_singular_3_m`,"
            +"`passive_past_singular_3_f`, `passive_past_dual_2_m`, `passive_past_dual_2_f`,"
            +"`passive_past_dual_3_m`, `passive_past_dual_3_f`, `passive_past_plural_1_m`,"
            +"`passive_past_plural_1_f`, `passive_past_plural_2_m`, `passive_past_plural_2_f`,"
            +"`passive_past_plural_3_m`, `passive_past_plural_3_f`, "
            +"`passive_none_past_singular_1_m`, `passive_none_past_singular_1_f`,"
            +"`passive_none_past_singular_2_m`, `passive_none_past_singular_2_f`,"
            +"`passive_none_past_singular_3_m`, `passive_none_past_singular_3_f`,"
            +"`passive_none_past_dual_2_m`, `passive_none_past_dual_2_f`,"
            +"`passive_none_past_dual_3_m`, `passive_none_past_dual_3_f`,"
            +"`passive_none_past_plural_1_m`, `passive_none_past_plural_1_f`,"
            +"`passive_none_past_plural_2_m`, `passive_none_past_plural_2_f`,"
            +"`passive_none_past_plural_3_m`, `passive_none_past_plural_3_f`,"
            +"`passive_subjunctive_singular_1_m`, `passive_subjunctive_singular_1_f`,"
            +"`passive_subjunctive_singular_2_m`, `passive_subjunctive_singular_2_f`,"
            +"`passive_subjunctive_singular_3_m`, `passive_subjunctive_singular_3_f`,"
            +"`passive_subjunctive_dual_2_m`, `passive_subjunctive_dual_2_f`,"
            +"`passive_subjunctive_dual_3_m`, `passive_subjunctive_dual_3_f`,"
            +"`passive_subjunctive_plural_1_m`, `passive_subjunctive_plural_1_f`,"
            +"`passive_subjunctive_plural_2_m`, `passive_subjunctive_plural_2_f`,"
            +"`passive_subjunctive_plural_3_m`, `passive_subjunctive_plural_3_f`,"
            +"`passive_jussive_singular_1_m`, `passive_jussive_singular_1_f`,"
            +"`passive_jussive_singular_2_m`, `passive_jussive_singular_2_f`,"
            +"`passive_jussive_singular_3_m`, `passive_jussive_singular_3_f`,"
            +"`passive_jussive_dual_2_m`, `passive_jussive_dual_2_f`,"
            +"`passive_jussive_dual_3_m`, `passive_jussive_dual_3_f`,"
            +"`passive_jussive_plural_1_m`, `passive_jussive_plural_1_f`,"
            +"`passive_jussive_plural_2_m`, `passive_jussive_plural_2_f`,"
            +"`passive_jussive_plural_3_m`, `passive_jussive_plural_3_f`"
            +") VALUES ("
            +"%(verb_root)s,"
            +"%(active_past_singular_1_m)s,"
            +"%(active_past_singular_1_f)s,"
            +"%(active_past_singular_2_m)s,"
            +"%(active_past_singular_2_f)s,"
            +"%(active_past_singular_3_m)s,"
            +"%(active_past_singular_3_f)s,"
            +"%(active_past_dual_2_m)s,"
            +"%(active_past_dual_2_f)s,"
            +"%(active_past_dual_3_m)s,"
            +"%(active_past_dual_3_f)s,"
            +"%(active_past_plural_1_m)s,"
            +"%(active_past_plural_1_f)s,"
            +"%(active_past_plural_2_m)s,"
            +"%(active_past_plural_2_f)s,"
            +"%(active_past_plural_3_m)s,"
            +"%(active_past_plural_3_f)s,"
            +"%(active_none_past_singular_1_m)s,"
            +"%(active_none_past_singular_1_f)s,"
            +"%(active_none_past_singular_2_m)s,"
            +"%(active_none_past_singular_2_f)s,"
            +"%(active_none_past_singular_3_m)s,"
            +"%(active_none_past_singular_3_f)s,"
            +"%(active_none_past_dual_2_m)s,"
            +"%(active_none_past_dual_2_f)s,"
            +"%(active_none_past_dual_3_m)s,"
            +"%(active_none_past_dual_3_f)s,"
            +"%(active_none_past_plural_1_m)s,"
            +"%(active_none_past_plural_1_f)s,"
            +"%(active_none_past_plural_2_m)s,"
            +"%(active_none_past_plural_2_f)s,"
            +"%(active_none_past_plural_3_m)s,"
            +"%(active_none_past_plural_3_f)s,"
            +"%(active_subjunctive_singular_1_m)s,"
            +"%(active_subjunctive_singular_1_f)s,"
            +"%(active_subjunctive_singular_2_m)s,"
            +"%(active_subjunctive_singular_2_f)s,"
            +"%(active_subjunctive_singular_3_m)s,"
            +"%(active_subjunctive_singular_3_f)s,"
            +"%(active_subjunctive_dual_2_m)s,"
            +"%(active_subjunctive_dual_2_f)s,"
            +"%(active_subjunctive_dual_3_m)s,"
            +"%(active_subjunctive_dual_3_f)s,"
            +"%(active_subjunctive_plural_1_m)s,"
            +"%(active_subjunctive_plural_1_f)s,"
            +"%(active_subjunctive_plural_2_m)s,"
            +"%(active_subjunctive_plural_2_f)s,"
            +"%(active_subjunctive_plural_3_m)s,"
            +"%(active_subjunctive_plural_3_f)s,"
            +"%(active_jussive_singular_1_m)s,"
            +"%(active_jussive_singular_1_f)s,"
            +"%(active_jussive_singular_2_m)s,"
            +"%(active_jussive_singular_2_f)s,"
            +"%(active_jussive_singular_3_m)s,"
            +"%(active_jussive_singular_3_f)s,"
            +"%(active_jussive_dual_2_m)s,"
            +"%(active_jussive_dual_2_f)s,"
            +"%(active_jussive_dual_3_m)s,"
            +"%(active_jussive_dual_3_f)s,"
            +"%(active_jussive_plural_1_m)s,"
            +"%(active_jussive_plural_1_f)s,"
            +"%(active_jussive_plural_2_m)s,"
            +"%(active_jussive_plural_2_f)s,"
            +"%(active_jussive_plural_3_m)s,"
            +"%(active_jussive_plural_3_f)s,"
            +"%(active_imperative_singular_2_m)s,"
            +"%(active_imperative_singular_2_f)s,"
            +"%(active_imperative_dual_2_m)s,"
            +"%(active_imperative_dual_2_f)s,"
            +"%(active_imperative_plural_2_m)s,"
            +"%(active_imperative_plural_2_f)s,"

            +"%(passive_past_singular_1_m)s,"
            +"%(passive_past_singular_1_f)s,"
            +"%(passive_past_singular_2_m)s,"
            +"%(passive_past_singular_2_f)s,"
            +"%(passive_past_singular_3_m)s,"
            +"%(passive_past_singular_3_f)s,"
            +"%(passive_past_dual_2_m)s,"
            +"%(passive_past_dual_2_f)s,"
            +"%(passive_past_dual_3_m)s,"
            +"%(passive_past_dual_3_f)s,"
            +"%(passive_past_plural_1_m)s,"
            +"%(passive_past_plural_1_f)s,"
            +"%(passive_past_plural_2_m)s,"
            +"%(passive_past_plural_2_f)s,"
            +"%(passive_past_plural_3_m)s,"
            +"%(passive_past_plural_3_f)s,"
            +"%(passive_none_past_singular_1_m)s,"
            +"%(passive_none_past_singular_1_f)s,"
            +"%(passive_none_past_singular_2_m)s,"
            +"%(passive_none_past_singular_2_f)s,"
            +"%(passive_none_past_singular_3_m)s,"
            +"%(passive_none_past_singular_3_f)s,"
            +"%(passive_none_past_dual_2_m)s,"
            +"%(passive_none_past_dual_2_f)s,"
            +"%(passive_none_past_dual_3_m)s,"
            +"%(passive_none_past_dual_3_f)s,"
            +"%(passive_none_past_plural_1_m)s,"
            +"%(passive_none_past_plural_1_f)s,"
            +"%(passive_none_past_plural_2_m)s,"
            +"%(passive_none_past_plural_2_f)s,"
            +"%(passive_none_past_plural_3_m)s,"
            +"%(passive_none_past_plural_3_f)s,"
            +"%(passive_subjunctive_singular_1_m)s,"
            +"%(passive_subjunctive_singular_1_f)s,"
            +"%(passive_subjunctive_singular_2_m)s,"
            +"%(passive_subjunctive_singular_2_f)s,"
            +"%(passive_subjunctive_singular_3_m)s,"
            +"%(passive_subjunctive_singular_3_f)s,"
            +"%(passive_subjunctive_dual_2_m)s,"
            +"%(passive_subjunctive_dual_2_f)s,"
            +"%(passive_subjunctive_dual_3_m)s,"
            +"%(passive_subjunctive_dual_3_f)s,"
            +"%(passive_subjunctive_plural_1_m)s,"
            +"%(passive_subjunctive_plural_1_f)s,"
            +"%(passive_subjunctive_plural_2_m)s,"
            +"%(passive_subjunctive_plural_2_f)s,"
            +"%(passive_subjunctive_plural_3_m)s,"
            +"%(passive_subjunctive_plural_3_f)s,"
            +"%(passive_jussive_singular_1_m)s,"
            +"%(passive_jussive_singular_1_f)s,"
            +"%(passive_jussive_singular_2_m)s,"
            +"%(passive_jussive_singular_2_f)s,"
            +"%(passive_jussive_singular_3_m)s,"
            +"%(passive_jussive_singular_3_f)s,"
            +"%(passive_jussive_dual_2_m)s,"
            +"%(passive_jussive_dual_2_f)s,"
            +"%(passive_jussive_dual_3_m)s,"
            +"%(passive_jussive_dual_3_f)s,"
            +"%(passive_jussive_plural_1_m)s,"
            +"%(passive_jussive_plural_1_f)s,"
            +"%(passive_jussive_plural_2_m)s,"
            +"%(passive_jussive_plural_2_f)s,"
            +"%(passive_jussive_plural_3_m)s,"
            +"%(passive_jussive_plural_3_f)s"
               ")")

    data = {
        'verb_root':verb_root ,
        'active_past_singular_1_m': active_past_singular_1_m,
        'active_past_singular_1_f': active_past_singular_1_f,
        'active_past_singular_2_m': active_past_singular_2_m,
        'active_past_singular_2_f': active_past_singular_2_f,
        'active_past_singular_3_m': active_past_singular_3_m,
        'active_past_singular_3_f': active_past_singular_3_f,
        'active_past_dual_2_m': active_past_dual_2_m,
        'active_past_dual_2_f': active_past_dual_2_f,
        'active_past_dual_3_m': active_past_dual_3_m,
        'active_past_dual_3_f': active_past_dual_3_f,
        'active_past_plural_1_m': active_past_plural_1_m,
        'active_past_plural_1_f': active_past_plural_1_f,
        'active_past_plural_2_m':active_past_plural_2_m ,
        'active_past_plural_2_f': active_past_plural_2_f,
        'active_past_plural_3_m': active_past_plural_3_m,
        'active_past_plural_3_f': active_past_plural_3_f,
        'active_none_past_singular_1_m':active_none_past_singular_1_m ,
        'active_none_past_singular_1_f':active_none_past_singular_1_f ,
        'active_none_past_singular_2_m':active_none_past_singular_2_m ,
        'active_none_past_singular_2_f':active_none_past_singular_2_f ,
        'active_none_past_singular_3_m':active_none_past_singular_3_m ,
        'active_none_past_singular_3_f':active_none_past_singular_3_f ,
        'active_none_past_dual_2_m':active_none_past_dual_2_m ,
        'active_none_past_dual_2_f': active_none_past_dual_2_f,
        'active_none_past_dual_3_m': active_none_past_dual_3_m,
        'active_none_past_dual_3_f':active_none_past_dual_3_f ,
        'active_none_past_plural_1_m': active_none_past_plural_1_m,
        'active_none_past_plural_1_f': active_none_past_plural_1_f,
        'active_none_past_plural_2_m': active_none_past_plural_2_m,
        'active_none_past_plural_2_f':active_none_past_plural_2_f ,
        'active_none_past_plural_3_m': active_none_past_plural_3_m,
        'active_none_past_plural_3_f': active_none_past_plural_3_f,
        'active_subjunctive_singular_1_m':active_subjunctive_singular_1_m ,
        'active_subjunctive_singular_1_f':active_subjunctive_singular_1_f ,
        'active_subjunctive_singular_2_m':active_subjunctive_singular_2_m ,
        'active_subjunctive_singular_2_f': active_subjunctive_singular_2_f,
        'active_subjunctive_singular_3_m': active_subjunctive_singular_3_m,
        'active_subjunctive_singular_3_f': active_subjunctive_singular_3_f,
        'active_subjunctive_dual_2_m':active_subjunctive_dual_2_m ,
        'active_subjunctive_dual_2_f':active_subjunctive_dual_2_f ,
        'active_subjunctive_dual_3_m':active_subjunctive_dual_3_m ,
        'active_subjunctive_dual_3_f': active_subjunctive_dual_3_f,
        'active_subjunctive_plural_1_m':active_subjunctive_plural_1_m ,
        'active_subjunctive_plural_1_f':active_subjunctive_plural_1_f ,
        'active_subjunctive_plural_2_m':active_subjunctive_plural_2_m ,
        'active_subjunctive_plural_2_f':active_subjunctive_plural_2_f ,
        'active_subjunctive_plural_3_m': active_subjunctive_plural_3_m,
        'active_subjunctive_plural_3_f':active_subjunctive_plural_3_f ,
        'active_jussive_singular_1_m': active_jussive_singular_1_m,
        'active_jussive_singular_1_f': active_jussive_singular_1_f,
        'active_jussive_singular_2_m':active_jussive_singular_2_m ,
        'active_jussive_singular_2_f':active_jussive_singular_2_f ,
        'active_jussive_singular_3_m':active_jussive_singular_3_m ,
        'active_jussive_singular_3_f':active_jussive_singular_3_f ,
        'active_jussive_dual_2_m':active_jussive_dual_2_m ,
        'active_jussive_dual_2_f':active_jussive_dual_2_f ,
        'active_jussive_dual_3_m':active_jussive_dual_3_m ,
        'active_jussive_dual_3_f':active_jussive_dual_3_f ,
        'active_jussive_plural_1_m': active_jussive_plural_1_m,
        'active_jussive_plural_1_f': active_jussive_plural_1_f,
        'active_jussive_plural_2_m': active_jussive_plural_2_m,
        'active_jussive_plural_2_f': active_jussive_plural_2_f,
        'active_jussive_plural_3_m':active_jussive_plural_3_m ,
        'active_jussive_plural_3_f':active_jussive_plural_3_f ,
        'active_imperative_singular_2_m':active_imperative_singular_2_m ,
        'active_imperative_singular_2_f':active_imperative_singular_2_f ,
        'active_imperative_dual_2_m': active_imperative_dual_2_m,
        'active_imperative_dual_2_f': active_imperative_dual_2_f,
        'active_imperative_plural_2_m': active_imperative_plural_2_m,
        'active_imperative_plural_2_f': active_imperative_plural_2_f,

        'passive_past_singular_1_m':passive_past_singular_1_m ,
        'passive_past_singular_1_f':passive_past_singular_1_f ,
        'passive_past_singular_2_m': passive_past_singular_2_m,
        'passive_past_singular_2_f': passive_past_singular_2_f,
        'passive_past_singular_3_m':passive_past_singular_3_m ,
        'passive_past_singular_3_f':passive_past_singular_3_f ,
        'passive_past_dual_2_m': passive_past_dual_2_m,
        'passive_past_dual_2_f': passive_past_dual_2_f,
        'passive_past_dual_3_m': passive_past_dual_3_m,
        'passive_past_dual_3_f': passive_past_dual_3_f,
        'passive_past_plural_1_m':passive_past_plural_1_m ,
        'passive_past_plural_1_f': passive_past_plural_1_f,
        'passive_past_plural_2_m': passive_past_plural_2_m,
        'passive_past_plural_2_f': passive_past_plural_2_f,
        'passive_past_plural_3_m': passive_past_plural_3_m,
        'passive_past_plural_3_f':passive_past_plural_3_f ,
        'passive_none_past_singular_1_m': passive_none_past_singular_1_m,
        'passive_none_past_singular_1_f': passive_none_past_singular_1_f,
        'passive_none_past_singular_2_m': passive_none_past_singular_2_m,
        'passive_none_past_singular_2_f': passive_none_past_singular_2_f,
        'passive_none_past_singular_3_m':passive_none_past_singular_3_m ,
        'passive_none_past_singular_3_f':passive_none_past_singular_3_f ,
        'passive_none_past_dual_2_m':passive_none_past_dual_2_m ,
        'passive_none_past_dual_2_f': passive_none_past_dual_2_f,
        'passive_none_past_dual_3_m': passive_none_past_dual_3_m,
        'passive_none_past_dual_3_f': passive_none_past_dual_3_f,
        'passive_none_past_plural_1_m':passive_none_past_plural_1_m ,
        'passive_none_past_plural_1_f':passive_none_past_plural_1_f ,
        'passive_none_past_plural_2_m':passive_none_past_plural_2_m ,
        'passive_none_past_plural_2_f':passive_none_past_plural_2_f ,
        'passive_none_past_plural_3_m':passive_none_past_plural_3_m ,
        'passive_none_past_plural_3_f':passive_none_past_plural_3_f ,
        'passive_subjunctive_singular_1_m': passive_subjunctive_singular_1_m,
        'passive_subjunctive_singular_1_f':passive_subjunctive_singular_1_f ,
        'passive_subjunctive_singular_2_m':passive_subjunctive_singular_2_m ,
        'passive_subjunctive_singular_2_f': passive_subjunctive_singular_2_f,
        'passive_subjunctive_singular_3_m': passive_subjunctive_singular_3_m,
        'passive_subjunctive_singular_3_f': passive_subjunctive_singular_3_f,
        'passive_subjunctive_dual_2_m':passive_subjunctive_dual_2_m ,
        'passive_subjunctive_dual_2_f': passive_subjunctive_dual_2_f,
        'passive_subjunctive_dual_3_m': passive_subjunctive_dual_3_m,
        'passive_subjunctive_dual_3_f': passive_subjunctive_dual_3_f,
        'passive_subjunctive_plural_1_m': passive_subjunctive_plural_1_m,
        'passive_subjunctive_plural_1_f': passive_subjunctive_plural_1_f,
        'passive_subjunctive_plural_2_m': passive_subjunctive_plural_2_m,
        'passive_subjunctive_plural_2_f': passive_subjunctive_plural_2_f,
        'passive_subjunctive_plural_3_m': passive_subjunctive_plural_3_m,
        'passive_subjunctive_plural_3_f': passive_subjunctive_plural_3_f,
        'passive_jussive_singular_1_m': passive_jussive_singular_1_m,
        'passive_jussive_singular_1_f': passive_jussive_singular_1_f,
        'passive_jussive_singular_2_m':passive_jussive_singular_2_m ,
        'passive_jussive_singular_2_f':passive_jussive_singular_2_f ,
        'passive_jussive_singular_3_m':passive_jussive_singular_3_m ,
        'passive_jussive_singular_3_f': passive_jussive_singular_3_f,
        'passive_jussive_dual_2_m': passive_jussive_dual_2_m,
        'passive_jussive_dual_2_f':passive_jussive_dual_2_f ,
        'passive_jussive_dual_3_m': passive_jussive_dual_3_m,
        'passive_jussive_dual_3_f': passive_jussive_dual_3_f,
        'passive_jussive_plural_1_m': passive_jussive_plural_1_m,
        'passive_jussive_plural_1_f':passive_jussive_plural_1_f ,
        'passive_jussive_plural_2_m': passive_jussive_plural_2_m,
        'passive_jussive_plural_2_f': passive_jussive_plural_2_f,
        'passive_jussive_plural_3_m': passive_jussive_plural_3_m,
        'passive_jussive_plural_3_f':passive_jussive_plural_3_f

    }
    cur.execute(query,data)
    return


mycursor.execute("SELECT * FROM `verbs_root`")

verb_root_rows = mycursor.fetchall()
error_count=0
for verb_root_row in verb_root_rows:
    print(str(verb_root_row['id']))
    try:


        file_path="verbs_tables/arabic_verb_"+str(verb_root_row['id'])+".html"
        verb_root=verb_root_row['verb_root']
        active_past_singular_1_m=None
        active_past_singular_1_f=None
        active_past_singular_2_m=None
        active_past_singular_2_f=None
        active_past_singular_3_m=None
        active_past_singular_3_f=None
        active_past_dual_2_m=None
        active_past_dual_2_f=None
        active_past_dual_3_m=None
        active_past_dual_3_f=None
        active_past_plural_1_m=None
        active_past_plural_1_f=None
        active_past_plural_2_m=None
        active_past_plural_2_f=None
        active_past_plural_3_m=None
        active_past_plural_3_f=None
        active_none_past_singular_1_m=None
        active_none_past_singular_1_f=None
        active_none_past_singular_2_m=None
        active_none_past_singular_2_f=None
        active_none_past_singular_3_m=None
        active_none_past_singular_3_f=None
        active_none_past_dual_2_m=None
        active_none_past_dual_2_f=None
        active_none_past_dual_3_m=None
        active_none_past_dual_3_f=None
        active_none_past_plural_1_m=None
        active_none_past_plural_1_f=None
        active_none_past_plural_2_m=None
        active_none_past_plural_2_f=None
        active_none_past_plural_3_m=None
        active_none_past_plural_3_f=None
        active_subjunctive_singular_1_m=None
        active_subjunctive_singular_1_f=None
        active_subjunctive_singular_2_m=None
        active_subjunctive_singular_2_f=None
        active_subjunctive_singular_3_m=None
        active_subjunctive_singular_3_f=None
        active_subjunctive_dual_2_m=None
        active_subjunctive_dual_2_f=None
        active_subjunctive_dual_3_m=None
        active_subjunctive_dual_3_f=None
        active_subjunctive_plural_1_m=None
        active_subjunctive_plural_1_f=None
        active_subjunctive_plural_2_m=None
        active_subjunctive_plural_2_f=None
        active_subjunctive_plural_3_m=None
        active_subjunctive_plural_3_f=None
        active_jussive_singular_1_m=None
        active_jussive_singular_1_f=None
        active_jussive_singular_2_m=None
        active_jussive_singular_2_f=None
        active_jussive_singular_3_m=None
        active_jussive_singular_3_f=None
        active_jussive_dual_2_m=None
        active_jussive_dual_2_f=None
        active_jussive_dual_3_m=None
        active_jussive_dual_3_f=None
        active_jussive_plural_1_m=None
        active_jussive_plural_1_f=None
        active_jussive_plural_2_m=None
        active_jussive_plural_2_f=None
        active_jussive_plural_3_m=None
        active_jussive_plural_3_f=None
        active_imperative_singular_2_m=None
        active_imperative_singular_2_f=None
        active_imperative_dual_2_m=None
        active_imperative_dual_2_f=None
        active_imperative_plural_2_m=None
        active_imperative_plural_2_f=None

        passive_past_singular_1_m=None
        passive_past_singular_1_f=None
        passive_past_singular_2_m=None
        passive_past_singular_2_f=None
        passive_past_singular_3_m=None
        passive_past_singular_3_f=None
        passive_past_dual_2_m=None
        passive_past_dual_2_f=None
        passive_past_dual_3_m=None
        passive_past_dual_3_f=None
        passive_past_plural_1_m=None
        passive_past_plural_1_f=None
        passive_past_plural_2_m=None
        passive_past_plural_2_f=None
        passive_past_plural_3_m=None
        passive_past_plural_3_f=None
        passive_none_past_singular_1_m=None
        passive_none_past_singular_1_f=None
        passive_none_past_singular_2_m=None
        passive_none_past_singular_2_f=None
        passive_none_past_singular_3_m=None
        passive_none_past_singular_3_f=None
        passive_none_past_dual_2_m=None
        passive_none_past_dual_2_f=None
        passive_none_past_dual_3_m=None
        passive_none_past_dual_3_f=None
        passive_none_past_plural_1_m=None
        passive_none_past_plural_1_f=None
        passive_none_past_plural_2_m=None
        passive_none_past_plural_2_f=None
        passive_none_past_plural_3_m=None
        passive_none_past_plural_3_f=None
        passive_subjunctive_singular_1_m=None
        passive_subjunctive_singular_1_f=None
        passive_subjunctive_singular_2_m=None
        passive_subjunctive_singular_2_f=None
        passive_subjunctive_singular_3_m=None
        passive_subjunctive_singular_3_f=None
        passive_subjunctive_dual_2_m=None
        passive_subjunctive_dual_2_f=None
        passive_subjunctive_dual_3_m=None
        passive_subjunctive_dual_3_f=None
        passive_subjunctive_plural_1_m=None
        passive_subjunctive_plural_1_f=None
        passive_subjunctive_plural_2_m=None
        passive_subjunctive_plural_2_f=None
        passive_subjunctive_plural_3_m=None
        passive_subjunctive_plural_3_f=None
        passive_jussive_singular_1_m=None
        passive_jussive_singular_1_f=None
        passive_jussive_singular_2_m=None
        passive_jussive_singular_2_f=None
        passive_jussive_singular_3_m=None
        passive_jussive_singular_3_f=None
        passive_jussive_dual_2_m=None
        passive_jussive_dual_2_f=None
        passive_jussive_dual_3_m=None
        passive_jussive_dual_3_f=None
        passive_jussive_plural_1_m=None
        passive_jussive_plural_1_f=None
        passive_jussive_plural_2_m=None
        passive_jussive_plural_2_f=None
        passive_jussive_plural_3_m=None
        passive_jussive_plural_3_f=None
        with codecs.open(file_path, "r", encoding="utf-8") as  f:
            dfs = pd.read_html(f.read())
            #print(len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][13]))))

            # active past for masculine with all number and person
            active_past_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][6]))[0] if  'nan' not in str(dfs[0][2][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][6]))) >0 else  None
            active_past_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][6]))[0] if  'nan' not in str(dfs[0][3][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][6]))) >0 else  None
            active_past_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][6]))[0] if  'nan' not in str(dfs[0][4][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][6]))) >0 else  None
            active_past_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][6]))[0] if  'nan' not in str(dfs[0][6][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][6]))) >0 else  None
            active_past_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][6]))[0] if  'nan' not in str(dfs[0][7][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][6]))) >0 else  None
            active_past_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][6]))[0] if  'nan' not in str(dfs[0][9][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][6]))) >0 else  None
            active_past_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][6]))[0] if  'nan' not in str(dfs[0][10][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][6]))) >0 else  None
            active_past_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][6]))[0] if  'nan' not in str(dfs[0][11][6]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][6]))) >0 else  None
            # active past for feminine with all number and person
            active_past_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][7]))[0] if  'nan' not in str(dfs[0][2][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][7]))) >0 else  None
            active_past_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][7]))[0] if  'nan' not in str(dfs[0][3][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][7]))) >0 else  None
            active_past_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][7]))[0] if  'nan' not in str(dfs[0][4][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][7]))) >0 else  None
            active_past_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][7]))[0] if  'nan' not in str(dfs[0][6][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][7]))) >0 else  None
            active_past_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][7]))[0] if  'nan' not in str(dfs[0][7][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][7]))) >0 else  None
            active_past_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][7]))[0] if  'nan' not in str(dfs[0][9][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][7]))) >0 else  None
            active_past_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][7]))[0] if  'nan' not in str(dfs[0][10][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][7]))) >0 else  None
            active_past_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][7]))[0] if  'nan' not in str(dfs[0][11][7]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][7]))) >0 else  None

            # active none-past for masculine with all number and person
            active_none_past_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][8]))[0] if  'nan' not in str(dfs[0][2][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][8]))) >0 else  None
            active_none_past_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][8]))[0] if  'nan' not in str(dfs[0][3][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][8]))) >0 else  None
            active_none_past_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][8]))[0] if  'nan' not in str(dfs[0][4][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][8]))) >0 else  None
            active_none_past_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][8]))[0] if  'nan' not in str(dfs[0][6][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][8]))) >0 else  None
            active_none_past_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][8]))[0] if  'nan' not in str(dfs[0][7][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][8]))) >0 else  None
            active_none_past_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][8]))[0] if  'nan' not in str(dfs[0][9][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][8]))) >0 else  None
            active_none_past_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][8]))[0] if  'nan' not in str(dfs[0][10][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][8]))) >0 else  None
            active_none_past_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][8]))[0] if  'nan' not in str(dfs[0][11][8]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][8]))) >0 else  None
            # active none-past for feminine with all number and person
            active_none_past_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][9]))[0] if  'nan' not in str(dfs[0][2][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][9]))) >0 else  None
            active_none_past_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][9]))[0] if  'nan' not in str(dfs[0][3][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][9]))) >0 else  None
            active_none_past_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][9]))[0] if  'nan' not in str(dfs[0][4][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][9]))) >0 else  None
            active_none_past_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][9]))[0] if  'nan' not in str(dfs[0][6][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][9]))) >0 else  None
            active_none_past_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][9]))[0] if  'nan' not in str(dfs[0][7][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][9]))) >0 else  None
            active_none_past_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][9]))[0] if  'nan' not in str(dfs[0][9][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][9]))) >0 else  None
            active_none_past_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][9]))[0] if  'nan' not in str(dfs[0][10][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][9]))) >0 else  None
            active_none_past_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][9]))[0] if  'nan' not in str(dfs[0][11][9]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][9]))) >0 else  None

            # active subjunctive for masculine with all number and person
            active_subjunctive_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][10]))[0] if  'nan' not in str(dfs[0][2][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][10]))) >0 else  None
            active_subjunctive_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][10]))[0] if  'nan' not in str(dfs[0][3][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][10]))) >0 else  None
            active_subjunctive_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][10]))[0] if  'nan' not in str(dfs[0][4][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][10]))) >0 else  None
            active_subjunctive_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][10]))[0] if  'nan' not in str(dfs[0][6][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][10]))) >0 else  None
            active_subjunctive_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][10]))[0] if  'nan' not in str(dfs[0][7][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][10]))) >0 else  None
            active_subjunctive_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][10]))[0] if  'nan' not in str(dfs[0][9][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][10]))) >0 else  None
            active_subjunctive_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][10]))[0] if  'nan' not in str(dfs[0][10][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][10]))) >0 else  None
            active_subjunctive_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][10]))[0] if  'nan' not in str(dfs[0][11][10]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][10]))) >0 else  None
            # active subjunctive for feminine with all number and person
            active_subjunctive_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][11]))[0] if  'nan' not in str(dfs[0][2][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][11]))) >0 else  None
            active_subjunctive_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][11]))[0] if  'nan' not in str(dfs[0][3][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][11]))) >0 else  None
            active_subjunctive_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][11]))[0] if  'nan' not in str(dfs[0][4][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][11]))) >0 else  None
            active_subjunctive_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][11]))[0] if  'nan' not in str(dfs[0][6][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][11]))) >0 else  None
            active_subjunctive_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][11]))[0] if  'nan' not in str(dfs[0][7][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][11]))) >0 else  None
            active_subjunctive_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][11]))[0] if  'nan' not in str(dfs[0][9][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][11]))) >0 else  None
            active_subjunctive_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][11]))[0] if  'nan' not in str(dfs[0][10][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][11]))) >0 else  None
            active_subjunctive_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][11]))[0] if  'nan' not in str(dfs[0][11][11]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][11]))) >0 else  None

            # active jussive for masculine with all number and person
            active_jussive_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][12]))[0] if  'nan' not in str(dfs[0][2][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][12]))) >0 else  None
            active_jussive_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][12]))[0] if  'nan' not in str(dfs[0][3][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][12]))) >0 else  None
            active_jussive_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][12]))[0] if  'nan' not in str(dfs[0][4][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][12]))) >0 else  None
            active_jussive_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][12]))[0] if  'nan' not in str(dfs[0][6][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][12]))) >0 else  None
            active_jussive_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][12]))[0] if  'nan' not in str(dfs[0][7][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][12]))) >0 else  None
            active_jussive_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][12]))[0] if  'nan' not in str(dfs[0][9][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][12]))) >0 else  None
            active_jussive_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][12]))[0] if  'nan' not in str(dfs[0][10][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][12]))) >0 else  None
            active_jussive_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][12]))[0] if  'nan' not in str(dfs[0][11][12]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][12]))) >0 else  None
            # active jussive for feminine with all number and person
            active_jussive_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][13]))[0] if  'nan' not in str(dfs[0][2][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][13]))) >0 else  None
            active_jussive_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][13]))[0] if  'nan' not in str(dfs[0][3][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][13]))) >0 else  None
            active_jussive_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][13]))[0] if  'nan' not in str(dfs[0][4][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][13]))) >0 else  None
            active_jussive_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][13]))[0] if  'nan' not in str(dfs[0][6][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][13]))) >0 else  None
            active_jussive_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][13]))[0] if  'nan' not in str(dfs[0][7][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][13]))) >0 else  None
            active_jussive_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][13]))[0] if  'nan' not in str(dfs[0][9][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][13]))) >0 else  None
            active_jussive_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][13]))[0] if  'nan' not in str(dfs[0][10][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][13]))) >0 else  None
            active_jussive_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][13]))[0] if  'nan' not in str(dfs[0][11][13]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][13]))) >0 else  None

            # active imperative for masculine with all number and person
            active_imperative_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][14]))[0] if  'nan' not in str(dfs[0][3][14]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][14]))) >0 else  None
            active_imperative_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][14]))[0] if  'nan' not in str(dfs[0][6][14]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][14]))) >0 else  None
            active_imperative_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][14]))[0] if  'nan' not in str(dfs[0][10][14]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][14]))) >0 else  None
            # active imperative for feminine with all number and person
            active_imperative_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][15]))[0] if  'nan' not in str(dfs[0][3][15]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][15]))) >0 else  None
            active_imperative_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][15]))[0] if  'nan' not in str(dfs[0][6][15]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][15]))) >0 else  None
            active_imperative_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][15]))[0] if  'nan' not in str(dfs[0][10][15]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][15]))) >0 else  None


            # passive past for masculine with all number and person
            passive_past_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][19]))[0] if  'nan' not in str(dfs[0][2][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][19]))) >0 else  None
            passive_past_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][19]))[0] if  'nan' not in str(dfs[0][3][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][19]))) >0 else  None
            passive_past_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][19]))[0] if  'nan' not in str(dfs[0][4][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][19]))) >0 else  None
            passive_past_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][19]))[0] if  'nan' not in str(dfs[0][6][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][19]))) >0 else  None
            passive_past_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][19]))[0] if  'nan' not in str(dfs[0][7][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][19]))) >0 else  None
            passive_past_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][19]))[0] if  'nan' not in str(dfs[0][9][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][19]))) >0 else  None
            passive_past_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][19]))[0] if  'nan' not in str(dfs[0][10][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][19]))) >0 else  None
            passive_past_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][19]))[0] if  'nan' not in str(dfs[0][11][19]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][19]))) >0 else  None
            # passive past for feminine with all number and person
            passive_past_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][20]))[0] if  'nan' not in str(dfs[0][2][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][20]))) >0 else  None
            passive_past_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][20]))[0] if  'nan' not in str(dfs[0][3][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][20]))) >0 else  None
            passive_past_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][20]))[0] if  'nan' not in str(dfs[0][4][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][20]))) >0 else  None
            passive_past_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][20]))[0] if  'nan' not in str(dfs[0][6][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][20]))) >0 else  None
            passive_past_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][20]))[0] if  'nan' not in str(dfs[0][7][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][20]))) >0 else  None
            passive_past_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][20]))[0] if  'nan' not in str(dfs[0][9][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][20]))) >0 else  None
            passive_past_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][20]))[0] if  'nan' not in str(dfs[0][10][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][20]))) >0 else  None
            passive_past_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][20]))[0] if  'nan' not in str(dfs[0][11][20]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][20]))) >0 else  None

            # passive none-past for masculine with all number and person
            passive_none_past_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][21]))[0] if  'nan' not in str(dfs[0][2][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][21]))) >0 else  None
            passive_none_past_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][21]))[0] if  'nan' not in str(dfs[0][3][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][21]))) >0 else  None
            passive_none_past_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][21]))[0] if  'nan' not in str(dfs[0][4][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][21]))) >0 else  None
            passive_none_past_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][21]))[0] if  'nan' not in str(dfs[0][6][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][21]))) >0 else  None
            passive_none_past_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][21]))[0] if  'nan' not in str(dfs[0][7][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][21]))) >0 else  None
            passive_none_past_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][21]))[0] if  'nan' not in str(dfs[0][9][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][21]))) >0 else  None
            passive_none_past_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][21]))[0] if  'nan' not in str(dfs[0][10][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][21]))) >0 else  None
            passive_none_past_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][21]))[0] if  'nan' not in str(dfs[0][11][21]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][21]))) >0 else  None
            # passive none-past for feminine with all number and person
            passive_none_past_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][22]))[0] if  'nan' not in str(dfs[0][2][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][22]))) >0 else  None
            passive_none_past_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][22]))[0] if  'nan' not in str(dfs[0][3][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][22]))) >0 else  None
            passive_none_past_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][22]))[0] if  'nan' not in str(dfs[0][4][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][22]))) >0 else  None
            passive_none_past_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][22]))[0] if  'nan' not in str(dfs[0][6][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][22]))) >0 else  None
            passive_none_past_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][22]))[0] if  'nan' not in str(dfs[0][7][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][22]))) >0 else  None
            passive_none_past_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][22]))[0] if  'nan' not in str(dfs[0][9][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][22]))) >0 else  None
            passive_none_past_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][22]))[0] if  'nan' not in str(dfs[0][10][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][22]))) >0 else  None
            passive_none_past_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][22]))[0] if  'nan' not in str(dfs[0][11][22]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][22]))) >0 else  None

            # passive subjunctive for masculine with all number and person
            passive_subjunctive_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][23]))[0] if  'nan' not in str(dfs[0][2][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][23]))) >0 else  None
            passive_subjunctive_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][23]))[0] if  'nan' not in str(dfs[0][3][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][23]))) >0 else  None
            passive_subjunctive_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][23]))[0] if  'nan' not in str(dfs[0][4][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][23]))) >0 else  None
            passive_subjunctive_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][23]))[0] if  'nan' not in str(dfs[0][6][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][23]))) >0 else  None
            passive_subjunctive_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][23]))[0] if  'nan' not in str(dfs[0][7][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][23]))) >0 else  None
            passive_subjunctive_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][23]))[0] if  'nan' not in str(dfs[0][9][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][23]))) >0 else  None
            passive_subjunctive_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][23]))[0] if  'nan' not in str(dfs[0][10][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][23]))) >0 else  None
            passive_subjunctive_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][23]))[0] if  'nan' not in str(dfs[0][11][23]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][23]))) >0 else  None
            # passive subjunctive for feminine with all number and person
            passive_subjunctive_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][24]))[0] if  'nan' not in str(dfs[0][2][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][24]))) >0 else  None
            passive_subjunctive_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][24]))[0] if  'nan' not in str(dfs[0][3][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][24]))) >0 else  None
            passive_subjunctive_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][24]))[0] if  'nan' not in str(dfs[0][4][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][24]))) >0 else  None
            passive_subjunctive_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][24]))[0] if  'nan' not in str(dfs[0][6][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][24]))) >0 else  None
            passive_subjunctive_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][24]))[0] if  'nan' not in str(dfs[0][7][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][24]))) >0 else  None
            passive_subjunctive_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][24]))[0] if  'nan' not in str(dfs[0][9][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][24]))) >0 else  None
            passive_subjunctive_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][24]))[0] if  'nan' not in str(dfs[0][10][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][24]))) >0 else  None
            passive_subjunctive_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][24]))[0] if  'nan' not in str(dfs[0][11][24]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][24]))) >0 else  None

            # passive jussive for masculine with all number and person
            passive_jussive_singular_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][25]))[0] if  'nan' not in str(dfs[0][2][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][25]))) >0 else  None
            passive_jussive_singular_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][25]))[0] if  'nan' not in str(dfs[0][3][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][25]))) >0 else  None
            passive_jussive_singular_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][25]))[0] if  'nan' not in str(dfs[0][4][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][25]))) >0 else  None
            passive_jussive_dual_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][25]))[0] if  'nan' not in str(dfs[0][6][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][25]))) >0 else  None
            passive_jussive_dual_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][25]))[0] if  'nan' not in str(dfs[0][7][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][25]))) >0 else  None
            passive_jussive_plural_1_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][25]))[0] if  'nan' not in str(dfs[0][9][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][25]))) >0 else  None
            passive_jussive_plural_2_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][25]))[0] if  'nan' not in str(dfs[0][10][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][25]))) >0 else  None
            passive_jussive_plural_3_m= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][25]))[0] if  'nan' not in str(dfs[0][11][25]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][25]))) >0 else  None
            # passive jussive for feminine with all number and person
            passive_jussive_singular_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][26]))[0] if  'nan' not in str(dfs[0][2][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][2][26]))) >0 else  None
            passive_jussive_singular_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][26]))[0] if  'nan' not in str(dfs[0][3][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][3][26]))) >0 else  None
            passive_jussive_singular_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][26]))[0] if  'nan' not in str(dfs[0][4][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][4][26]))) >0 else  None
            passive_jussive_dual_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][26]))[0] if  'nan' not in str(dfs[0][6][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][6][26]))) >0 else  None
            passive_jussive_dual_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][26]))[0] if  'nan' not in str(dfs[0][7][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][7][26]))) >0 else  None
            passive_jussive_plural_1_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][26]))[0] if  'nan' not in str(dfs[0][9][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][9][26]))) >0 else  None
            passive_jussive_plural_2_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][26]))[0] if  'nan' not in str(dfs[0][10][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][10][26]))) >0 else None
            passive_jussive_plural_3_f= re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][26]))[0] if  'nan' not in str(dfs[0][11][26]) and len(re.findall(r'[\u0600-\u06FF]+', remove_diacritics(dfs[0][11][26]))) >0 else  None


            insert_verb_inflection( verb_root,
                               active_past_singular_1_m,
                               active_past_singular_1_f,
                               active_past_singular_2_m,
                               active_past_singular_2_f,
                               active_past_singular_3_m,
                               active_past_singular_3_f,
                               active_past_dual_2_m,
                               active_past_dual_2_f,
                               active_past_dual_3_m,
                               active_past_dual_3_f,
                               active_past_plural_1_m,
                               active_past_plural_1_f,
                               active_past_plural_2_m,
                               active_past_plural_2_f,
                               active_past_plural_3_m,
                               active_past_plural_3_f,
                               active_none_past_singular_1_m,
                               active_none_past_singular_1_f,
                               active_none_past_singular_2_m,
                               active_none_past_singular_2_f,
                               active_none_past_singular_3_m,
                               active_none_past_singular_3_f,
                               active_none_past_dual_2_m,
                               active_none_past_dual_2_f,
                               active_none_past_dual_3_m,
                               active_none_past_dual_3_f,
                               active_none_past_plural_1_m,
                               active_none_past_plural_1_f,
                               active_none_past_plural_2_m,
                               active_none_past_plural_2_f,
                               active_none_past_plural_3_m,
                               active_none_past_plural_3_f,
                               active_subjunctive_singular_1_m,
                               active_subjunctive_singular_1_f,
                               active_subjunctive_singular_2_m,
                               active_subjunctive_singular_2_f,
                               active_subjunctive_singular_3_m,
                               active_subjunctive_singular_3_f,
                               active_subjunctive_dual_2_m,
                               active_subjunctive_dual_2_f,
                               active_subjunctive_dual_3_m,
                               active_subjunctive_dual_3_f,
                               active_subjunctive_plural_1_m,
                               active_subjunctive_plural_1_f,
                               active_subjunctive_plural_2_m,
                               active_subjunctive_plural_2_f,
                               active_subjunctive_plural_3_m,
                               active_subjunctive_plural_3_f,
                               active_jussive_singular_1_m,
                               active_jussive_singular_1_f,
                               active_jussive_singular_2_m,
                               active_jussive_singular_2_f,
                               active_jussive_singular_3_m,
                               active_jussive_singular_3_f,
                               active_jussive_dual_2_m,
                               active_jussive_dual_2_f,
                               active_jussive_dual_3_m,
                               active_jussive_dual_3_f,
                               active_jussive_plural_1_m,
                               active_jussive_plural_1_f,
                               active_jussive_plural_2_m,
                               active_jussive_plural_2_f,
                               active_jussive_plural_3_m,
                               active_jussive_plural_3_f,
                               active_imperative_singular_2_m,
                               active_imperative_singular_2_f,
                               active_imperative_dual_2_m,
                               active_imperative_dual_2_f,
                               active_imperative_plural_2_m,
                               active_imperative_plural_2_f,

                               passive_past_singular_1_m,
                               passive_past_singular_1_f,
                               passive_past_singular_2_m,
                               passive_past_singular_2_f,
                               passive_past_singular_3_m,
                               passive_past_singular_3_f,
                               passive_past_dual_2_m,
                               passive_past_dual_2_f,
                               passive_past_dual_3_m,
                               passive_past_dual_3_f,
                               passive_past_plural_1_m,
                               passive_past_plural_1_f,
                               passive_past_plural_2_m,
                               passive_past_plural_2_f,
                               passive_past_plural_3_m,
                               passive_past_plural_3_f,
                               passive_none_past_singular_1_m,
                               passive_none_past_singular_1_f,
                               passive_none_past_singular_2_m,
                               passive_none_past_singular_2_f,
                               passive_none_past_singular_3_m,
                               passive_none_past_singular_3_f,
                               passive_none_past_dual_2_m,
                               passive_none_past_dual_2_f,
                               passive_none_past_dual_3_m,
                               passive_none_past_dual_3_f,
                               passive_none_past_plural_1_m,
                               passive_none_past_plural_1_f,
                               passive_none_past_plural_2_m,
                               passive_none_past_plural_2_f,
                               passive_none_past_plural_3_m,
                               passive_none_past_plural_3_f,
                               passive_subjunctive_singular_1_m,
                               passive_subjunctive_singular_1_f,
                               passive_subjunctive_singular_2_m,
                               passive_subjunctive_singular_2_f,
                               passive_subjunctive_singular_3_m,
                               passive_subjunctive_singular_3_f,
                               passive_subjunctive_dual_2_m,
                               passive_subjunctive_dual_2_f,
                               passive_subjunctive_dual_3_m,
                               passive_subjunctive_dual_3_f,
                               passive_subjunctive_plural_1_m,
                               passive_subjunctive_plural_1_f,
                               passive_subjunctive_plural_2_m,
                               passive_subjunctive_plural_2_f,
                               passive_subjunctive_plural_3_m,
                               passive_subjunctive_plural_3_f,
                               passive_jussive_singular_1_m,
                               passive_jussive_singular_1_f,
                               passive_jussive_singular_2_m,
                               passive_jussive_singular_2_f,
                               passive_jussive_singular_3_m,
                               passive_jussive_singular_3_f,
                               passive_jussive_dual_2_m,
                               passive_jussive_dual_2_f,
                               passive_jussive_dual_3_m,
                               passive_jussive_dual_3_f,
                               passive_jussive_plural_1_m, 
                               passive_jussive_plural_1_f,
                               passive_jussive_plural_2_m,
                               passive_jussive_plural_2_f,
                               passive_jussive_plural_3_m,
                               passive_jussive_plural_3_f)
    except Exception as e:
        print("error",e)
        error_count+=1


mysql.commit()
print(error_count)
