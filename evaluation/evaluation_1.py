# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 17:25:21 2020

@author: WAEL
"""
original_sentence="بالإضافة إلى 03 ‬أغنية داخل الأحداث"

inflected_sentence="بالإضافة إلى "

import requests
import json

url = 'http://127.0.0.1:5000/ar_countable'
myobj = {
'count':'30',
'noun':'أغنيات',
'gender':'',
'case':'',
'dual':'',
'plural':'',
'number_format':'digitsOnly',
'zero_format':'',
'modifiers':'',
'agreement':''}

page = requests.post(url, data = myobj)

output = json.loads(page.text)


if not output["error"]:
    #print(output["result"])
    inflected_sentence+=output["result"]
else:
    print("Error")
    
inflected_sentence+=" داخل ال"

url = 'http://127.0.0.1:5000/ar_inflectNoun'
myobj = {
'number':'3',
'word':'حدث',
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