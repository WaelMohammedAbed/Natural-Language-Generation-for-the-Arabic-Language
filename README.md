# Natural Language Generation for the Arabic Language
This repo is to provide the source code and the evaluation of the paper "Arabic NLG Language Functions" which was accepted to be published in "The 13th International Conference on Natural Language Generation (INLG 2020)". It is also part of my final project in order to get a degree in MSc of AI at the University of Aberdeen

## The Arabic language functions API (introduction)
This API consists of 8 Arabic language functions and provided with web UI with documentation
and a few examples on how to use it. It can be run locally or by accessing this live website
(https://ar-nlg.herokuapp.com/).

## Using the Arabic language functions API

The API can be used either by accessing the live website or by installing it locally and run it (refer
to the installation manual in the next chapter). The website home page is the index page with
the links and documentation of all the functions (see the figure below). All the functions have a
similar procedure to use, first click the link (name) of the wanted function in the home page. This
will redirect you to the specified user interface (UI) of the function. Fill the fields with the desired
values then click enter to get the results. Moreover, each function provided with few examples to
illustrates what values should each field take and how it works.

## Getting Started (what you need)

- A computer device with Python 3 installed.
- The Wamp server is installed and running.
- A web browser. Preferred Chrome as the system was tested using this browser.

## Setting Up the Arabic language functions API
To set up the API first you need to import the DB for the Arabic lexicon. To do this follow these
steps:
- Make sure that the Wamp server is installed and running.
- Open the web browser then enter this URL (http://localhost/phpmyadmin/index.php). This will open the “PHPMyAdmin” page where you can connect to the MySQL DB
engine.
- Enter username, password and choose MySQL as your DB server. These values should be
set during the installation of the Wamp server, by default, the values are “root” for username
and an empty password.
- In the next page create new DB. Set the DB name to "ar_nlg" and choose "utf8_unicode_ci" to support Arabic letters encoding.
- Choose the created DB, then from the menu click on Import, after that, click on “choose
file” button and locate the MySQL file provided in the zipped file “/code/data/mysql_db/
ar_nlg.sql”. finally, click the “Go” button at the bottom of the page. This will run the scripts
in the file and insert all the 9000 entries and all their tables.
- Now that the lexicon is ready, and Python 3 is installed. We can start running the API.

## Running the Arabic language function API

These are the list of instructions needed to run the API. These instructions apply to devices with
Windows operating system:

First, unzip the code zipped file then navigate to the "api" folder.
- Open "db.yaml" file and update the database configuration to match the value you entered
during the installation phase. By default this file has these values(mysql_host: ’localhost’,
mysql_user: ’root’, mysql_password: ”, mysql_,db: ’ar_nlg’).
 - Inside the "api" folder open a command prompt window and run this command "virtualenv
env" to create a virtual environment for this API.
 - Then, run this command "envScriptsactivate" to activate the virtual environment.
- if an error occurred during the activation of the virtual environment. then it is more likely
because of the windows restriction policies. To overcome this error run this command "Set-
ExecutionPolicy Unrestricted -Force".
- To install all the required libraries, run this command "pip install -r requirements.txt".
- That is it. to run the API, run this command "python app.py".
- By default, this will run a web host service with the API running on this URL "http://127.0.0.1:5000/". Open
any web browser and insert this URL to see the API




## License
[MIT](https://choosealicense.com/licenses/mit/)
