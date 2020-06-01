from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as MySQL

import countable_nouns as cn
import ar_inflectVerb as iv

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
@app.route('/inflect_verbs', methods=['GET', 'POST'])
def inflect_verbs():
    return render_template('inflect_verbs.html')
@app.route('/add_noun', methods=['GET', 'POST'])
def add_noun():
    if request.method == 'POST':
        # Fetch form data
        nounDetails = request.form
        singular = nounDetails['singular']
        gender = nounDetails['gender']
        dual_a = nounDetails['dual_a']
        dual_n = nounDetails['dual_n']
        dual_g = nounDetails['dual_g']
        plural_a = nounDetails['plural_a']
        plural_n = nounDetails['plural_n']
        plural_g = nounDetails['plural_g']
        cur = mysql.cursor()
        cur.execute("INSERT INTO `nouns`( `singular`, `gender`, `dual_a`, `dual_n`, `dual_g`, `plural_a`, `plural_n`, `plural_g`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(singular, gender, dual_a, dual_n, dual_g, plural_a, plural_n, plural_g))
        mysql.commit()
        cur.close()
        return redirect('/nouns')
    return render_template('add_noun.html')

@app.route('/nouns')
def users():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM `nouns`")
    nouns = cur.fetchall()
    return render_template('nouns.html',nouns=nouns)
    
@app.route('/get_noun_details/<string:singular>',methods=['GET'])
def get_noun_details(singular):
    cur = mysql.cursor()
    select_singular=("SELECT * FROM `nouns` WHERE `singular` = %(singular)s")
    data_singular = {
      'singular': singular,
    }
    cur.execute(select_singular,data_singular)
    noun = cur.fetchall()
    if len(noun)>0:
        return jsonify({ 'singular':noun[0][1], 'gender':noun[0][2], 'dual_a':noun[0][3], 'dual_n':noun[0][4], 'dual_g':noun[0][5], 'plural_a':noun[0][6], 'plural_n':noun[0][7], 'plural_g':noun[0][8]})
    else:
        return jsonify({ 'error':'not found'})

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
        
        
        print(count,noun,case,gender,dual,plural,number_format,zero_format,modifiers,agreement)
    #def Countable(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر"):
        countable_noun_printable=cn.countable(count,noun,case,gender,dual,plural,number_format,zero_format,modifiers,agreement)
        return jsonify(countable_noun_printable)
    return jsonify({ 'error':True, 'message':'wrong request'});
    
@app.route('/ar_inflectVerb', methods=['GET', 'POST'])
def ar_inflectVerb():
    if request.method == 'POST':
        # Fetch form data
        postDetails = request.form
        word = postDetails['word']
        word=str(word).strip()
        
        number = postDetails['number']
        try:
            number = int(number)
            if(number ==1):
                number="singular"
            elif(number == 2):
                number="dual"
            elif(number > 2):
                number = "plural"
            else:
                return jsonify({ 'error':True, 'message':' number field value is not valid'});
        except ValueError:
            number=str(number)
        person = postDetails['person']
        person=str(person).strip()
        try:
            person = int(person)
             
        except ValueError:
            return jsonify({ 'error':True, 'message':' person field value is not valid'});
            
        gender = postDetails['gender']
        gender=str(gender).strip()
        
        voice = postDetails['voice']
        voice=str(voice).strip()
        mood_tense = postDetails['mood_tense']
        mood_tense=str(mood_tense).strip()
        
        
        print(word,number,gender,person,voice,mood_tense)
    #def Countable(count, noun, case="nominative", gender = None, dual = None, plural = None, number_format = "wordsOnly", zero_format = "صفر"):
        ar_inflectVerb_printable=iv.ar_inflectVerb(word,number,gender,person,voice,mood_tense)
        return jsonify(ar_inflectVerb_printable)
    return jsonify({ 'error':True, 'message':'wrong request'});

if __name__ == '__main__':
    app.run(debug=True)
