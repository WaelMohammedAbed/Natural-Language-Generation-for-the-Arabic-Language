# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 17:25:21 2020

@author: WAEL
"""
original_sentence="بررت ساندي اتهاماتها لقرارها بسحب الأغنية "

inflected_sentence=""

import requests
import json

# get inflected verb from the API
url = 'http://127.0.0.1:5000/ar_inflectVerb'
myobj = {
'word':'برر',
'number': '1',
'gender': 'f',
'person': '3',
'mood_tense': 'past',
'voice': 'active'}

page = requests.post(url, data = myobj)

output = json.loads(page.text)


if not output["error"]:
    #print(output["result"])
    inflected_sentence+=output["result"]
else:
    print("Error")
# ---------------------------------------------------

inflected_sentence+=" ساندي "

# get inflected noun from the API
url = 'http://127.0.0.1:5000/ar_inflectNoun'
myobj = {
'word':'اتهام',
'number': 'plural',
'gender': 'f',
'case': '',
'dual': '',
'plural': ''}

page = requests.post(url, data = myobj)

output = json.loads(page.text)

noun_1=""
if not output["error"]:
    #print(output["result"])
    noun_1=output["result"]
else:
    print("Error")
# ---------------------------------------------------

# add possessive pronoun to the noun resulted from the previous call
url = 'http://127.0.0.1:5000/ar_pronouns'
myobj = {
'word':noun_1,
'number': '1',
'gender': 'f',
'pronoun_type': 'possessive',
'is_person': '',
'person': '3'}

page = requests.post(url, data = myobj)

#print(page.text)
output = json.loads(page.text)


if not output["error"]:
    #print(output["result"])
    inflected_sentence+=output["result"]
else:
    print("Error")
# ---------------------------------------------------
inflected_sentence+=" ل"

# get inflected noun from the API
url = 'http://127.0.0.1:5000/ar_inflectNoun'
myobj = {
'word':'قرار',
'number': 'singular',
'gender': '',
'case': '',
'dual': '',
'plural': ''}

page = requests.post(url, data = myobj)

output = json.loads(page.text)

noun_2=""
if not output["error"]:
    #print(output["result"])
    noun_2=output["result"]
else:
    print("Error1")
    print(page.text)
# ---------------------------------------------------

# add possessive pronoun to the noun resulted from the previous call
url = 'http://127.0.0.1:5000/ar_pronouns'
myobj = {
'word':noun_2,
'number': '1',
'gender': 'f',
'pronoun_type': 'possessive',
'is_person': '',
'person': '3'}

page = requests.post(url, data = myobj)

output = json.loads(page.text)


if not output["error"]:
    #print(output["result"])
    inflected_sentence+=output["result"]
else:
    print("Error1")
    print(page.text)
# ---------------------------------------------------

   
inflected_sentence+=" بسحب ال"

url = 'http://127.0.0.1:5000/ar_inflectNoun'
myobj = {
'number':'1',
'word':'أغنية',
'gender':'',
'case':'',
'dual':'',
'plural':''}

page = requests.post(url, data = myobj)



output = json.loads(page.text)

if not output["error"]:
    #print(output["result"])
    inflected_sentence+=output["result"]
else:
    #print(page.text)
    print("Error")
    
print(original_sentence)
print(inflected_sentence)