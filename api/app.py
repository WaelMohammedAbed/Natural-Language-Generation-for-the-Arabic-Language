from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as MySQL

import countable_nouns as cn
import ar_inflectVerb as iverb
import ar_inflectNoun as inoun
import ar_inflectAdjective as iadjective
import ar_pronouns as ar_p

import yaml

app = Flask(__name__)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL.connect(host=db['mysql_host'],database=db['mysql_db'],user=db['mysql_user'],password=db['mysql_password'])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/countable_nouns', methods=['GET', 'POST'])
def countable_nouns():
    return render_template('countable.html')

@app.route('/inflect_noun', methods=['GET', 'POST'])
def inflect_noun():
    return render_template('inflect_noun.html')

@app.route('/inflect_adjective', methods=['GET', 'POST'])
def inflect_adjective():
    return render_template('inflect_adjective.html')

@app.route('/inflect_verbs', methods=['GET', 'POST'])
def inflect_verbs():
    return render_template('inflect_verbs.html')

@app.route('/pronouns', methods=['GET', 'POST'])
def pronouns():
    return render_template('pronouns.html')


@app.route('/ar_countable', methods=['GET', 'POST'])
def ar_countable():
    if request.method == 'POST':
        # Fetch form data
        nounDetails = request.form
        count = nounDetails['count']
        count=str(count).strip()
        try:
            count = int(count)
        except ValueError:
            count=str(count)
        noun = nounDetails['noun']
        noun=str(noun).strip()
        if len(str(count)) ==0 or len(noun) == 0:
            return jsonify({ 'error':True, 'message':'count and noun are mandatory'});

        case = nounDetails['case']
        case=str(case).strip()
        if len(case) ==0:
            case= "nominative"
        elif case != "nominative" and case != "accusative" and case != "genitive":
            return jsonify({ 'error':True, 'message':' case field can take only one of these values (nominative, accusative or genitive)'});

        gender = nounDetails['gender']
        gender=str(gender).strip()
        try:
            gender = int(gender)
        except ValueError:
            gender=str(gender)
        if len(str(gender)) ==0:
            gender= None
        elif gender == "Male" or gender == "male" or gender == "True" or gender == "true" or gender == "1" or gender == 1:
            gender = 1
        elif gender == "Female" or gender == "female" or gender == "False" or gender == "false" or gender == "0" or gender == 0:
            gender = 0
        else:
            return jsonify({ 'error':True, 'message':' Gender ('+str(gender)+') field can take only one of these values (True, False, 1 or 0 )'});

        dual = nounDetails['dual']
        dual=str(dual).strip()
        if len(dual) ==0:
            dual= None

        plural = nounDetails['plural']
        plural=str(plural).strip()
        if len(plural) ==0:
            plural= None

        number_format = nounDetails['number_format']
        number_format=str(number_format).strip()
        try:
            number_format = int(number_format)
        except ValueError:
            if len(number_format) ==0:
                number_format= "wordsOnly"
            elif number_format != "wordsOnly" and number_format != "digitsOnly":
                return jsonify({ 'error':True, 'message':' Number Format field can take only one of these values (digitsOnly, wordsOnly or a number)'});

        zero_format = nounDetails['zero_format']
        zero_format=str(zero_format).strip()
        if len(zero_format) ==0:
            zero_format= "صفر"
        modifiers_str = nounDetails['modifiers']
        modifiers_str=str(modifiers_str).strip()
        modifiers=[]
        if len(modifiers_str) ==0:
            modifiers= []
        else:
            for modifier in modifiers_str.split(","):
                modifiers.append(modifier.strip())

        agreement = nounDetails['agreement']
        agreement=str(agreement).strip()
        try:
            agreement = int(agreement)
        except ValueError:
            agreement=str(agreement)
        if len(str(agreement)) ==0:
            agreement= 1
        elif agreement == "FA" or agreement == "fa" or agreement == "True" or agreement == "true" or agreement == "1" or agreement == 1:
            agreement = 1
        elif agreement == "DA" or agreement == "da" or agreement == "False" or agreement == "false" or agreement == "0" or agreement == 0:
            agreement = 0
        else:
            return jsonify({ 'error':True, 'message':' agreement ('+str(agreement)+') field can take only one of these values (FA, DA, 1 or 0 )'});


        countable_noun_printable=cn.countable(count,noun,case,gender,dual,plural,number_format,zero_format,modifiers,agreement)
        return jsonify(countable_noun_printable)
    return jsonify({ 'error':True, 'message':'wrong request'});

@app.route('/ar_inflectVerb', methods=['GET', 'POST'])
def ar_inflectVerb():
    if request.method == 'POST':
        # Fetch form data
        postDetails = request.form
        word = postDetails['word']

        number = postDetails['number']
        person = postDetails['person']
        gender = postDetails['gender']
        voice = postDetails['voice']
        mood_tense = postDetails['mood_tense']


    #def Countable(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر"):
        ar_inflectVerb_printable=iverb.ar_inflectVerb(word,number,gender,person,voice,mood_tense)
        return jsonify(ar_inflectVerb_printable)
    return jsonify({ 'error':True, 'message':'wrong request'});


@app.route('/ar_inflectNoun', methods=['GET', 'POST'])
def ar_inflectNoun():
    if request.method == 'POST':
        # Fetch form data
        postDetails = request.form
        word = postDetails['word']
        word=str(word).strip()

        number = postDetails['number']

        gender = postDetails['gender']

        case = postDetails['case']

        dual = postDetails['dual']

        plural = postDetails['plural']



        ar_inflectNoun_printable=inoun.ar_inflectNoun(number,word,case,gender,dual,plural)
        return jsonify(ar_inflectNoun_printable)
    return jsonify({ 'error':True, 'message':'wrong request'});


@app.route('/ar_inflectAdjective', methods=['GET', 'POST'])
def ar_inflectAdjective():
    if request.method == 'POST':
        # Fetch form data
        try:
            postDetails = request.form
            agreement = postDetails['agreement']

            number = postDetails['number']

            gender = postDetails['gender']

            case = postDetails['case']
            is_human = postDetails['is_human']

            modifiers_str = postDetails['modifiers']
            ar_inflectVerb_printable=iadjective.inflectAdjectives(modifiers_str,number,case,gender,is_human,agreement)
            return jsonify(ar_inflectVerb_printable)
        except  Exception as e:
            return jsonify({ 'error':True, 'message':'post values not found '+str(e)});
    return jsonify({ 'error':True, 'message':'wrong request'});


@app.route('/ar_pronouns', methods=['GET', 'POST'])
def ar_pronouns():
    if request.method == 'POST':
        # Fetch form data
        postDetails = request.form
        word = postDetails['word']

        number = postDetails['number']

        person = postDetails['person']

        gender = postDetails['gender']

        pronoun_type = postDetails['pronoun_type']
        is_person = postDetails['is_person']



        ar_pronoun_printable=ar_p.ar_pronoun(number,gender,person,pronoun_type,word,is_person)
        return jsonify(ar_pronoun_printable)
    return jsonify({ 'error':True, 'message':'wrong request'});

if __name__ == '__main__':
    app.run(debug=True)
