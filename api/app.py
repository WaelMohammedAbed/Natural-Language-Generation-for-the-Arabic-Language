from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as MySQL

import countable_nouns as cn
import ar_inflectVerb as iverb
import ar_inflectNoun as inoun
import ar_inflectAdjective as iadjective
import ar_pronouns as ar_p
import ar_numToWords as ntw
import ar_countryAdjective as cAdjective
import ar_countryDeterminer as cDeterminer

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

@app.route('/num_to_words', methods=['GET', 'POST'])
def num_to_words():
    return render_template('num_to_words.html')

@app.route('/country_adjective', methods=['GET', 'POST'])
def country_adjective():
    return render_template('country_adjective.html')

@app.route('/country_determiner', methods=['GET', 'POST'])
def country_determiner():
    return render_template('country_determiner.html')


@app.route('/ar_countable', methods=['GET', 'POST'])
def ar_countable():
    if request.method == 'POST':
        # Fetch form data
        nounDetails = request.form
        count = nounDetails['count']

        noun = nounDetails['noun']
        case = nounDetails['case']
        gender = nounDetails['gender']
        gender=str(gender).strip()
        dual = nounDetails['dual']
        plural = nounDetails['plural']
        number_format = nounDetails['number_format']

        zero_format = nounDetails['zero_format']
        modifiers_str = nounDetails['modifiers']
        agreement = nounDetails['agreement']


        countable_noun_printable=cn.countable(count,noun,case,gender,dual,plural,number_format,zero_format,modifiers_str,agreement)
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

@app.route('/ar_numToWords', methods=['GET', 'POST'])
def ar_numToWords():
    if request.method == 'POST':
        # Fetch form data
        nounDetails = request.form
        count = nounDetails['count']
        case = nounDetails['case']
        gender = nounDetails['gender']
        numbers_type = nounDetails['type']
        number_format = nounDetails['number_format']

        zero_format = nounDetails['zero_format']
        numToWords_printable=ntw.ar_numToWords(count,case,gender,numbers_type,number_format,zero_format)
        return jsonify(numToWords_printable)
    return jsonify({ 'error':True, 'message':'wrong request'});

@app.route('/ar_countryAdjective', methods=['GET', 'POST'])
def ar_countryAdjective():
    if request.method == 'POST':
        # Fetch form data
        try:
            postDetails = request.form

            number = postDetails['number']
            gender = postDetails['gender']
            case = postDetails['case']
            country = postDetails['country']

            ar_inflectVerb_printable=cAdjective.ar_countryAdjective(country,number,case,gender)
            return jsonify(ar_inflectVerb_printable)
        except  Exception as e:
            return jsonify({ 'error':True, 'message':'post values not found '+str(e)});
    return jsonify({ 'error':True, 'message':'wrong request'});

@app.route('/ar_countryDeterminer', methods=['GET', 'POST'])
def ar_countryDeterminer():
    if request.method == 'POST':
        # Fetch form data
        try:
            postDetails = request.form

            country = postDetails['country']

            ar_inflectVerb_printable=cDeterminer.ar_countryDeterminer(country)
            return jsonify(ar_inflectVerb_printable)
        except  Exception as e:
            return jsonify({ 'error':True, 'message':'post values not found '+str(e)});
    return jsonify({ 'error':True, 'message':'wrong request'});


if __name__ == '__main__':
    app.run(debug=True)
