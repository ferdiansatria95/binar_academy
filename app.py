#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import sqlite3
import re
from flask import Flask, jsonify, request, make_response
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import swag_from

import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


app = Flask(__name__)
app.json_encoder = LazyJSONEncoder


database = sqlite3.connect('data/new_db_tweet.db', check_same_thread = False)
database.row_factory = sqlite3.Row
mycursor = database.cursor()
database.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, text_old varchar(255), text_cleaned varchar(255));''')


swagger_template = dict(
info = {
    'title':LazyString(lambda: 'API Documentation for Tweet Cleaner'),
    'version':LazyString(lambda : '1.0.0'),
    'description':LazyString(lambda : 'Use this API for cleaning your tweet'),
},
    host = LazyString(lambda:request.host)
    
)

swagger_config = {
    "headers":[],
    "specs":[
        {'endpoint':'docs',
        'route':'/docs.json',
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui":True,
    "specs_route":"/docs"
    
}

swagger = Swagger(app,template=swagger_template,
                 config=swagger_config)

@swag_from("docs/welcome_page.yml",methods=['GET'])
@app.route('/',methods=['GET'])
def welcome():
    return "Welcoming to Tweet Cleaner"

@swag_from("docs/input_text.yml", methods=['POST'])
@app.route('/data_text',methods=['POST'])
def data_text():
    if request.method == 'POST':
        text = str(request.form['text'])
        text_clean = text.lower()
        text_clean = re.sub('user','',text_clean)
        text_clean = re.sub('rt :','',text_clean)
        text_clean = re.sub(r'^\n\n',' ',text_clean)
        text_clean = re.sub('\d.*.$','',text_clean)
        text_clean = re.sub('\A.*\\\\n',' ',text_clean)
        text_clean = re.sub(r'^\\x[0-9a-zA-Z]','',text_clean)
        text_clean = re.sub('\A.*https','',text_clean)
        text_clean = re.sub(' +',' ',text_clean)
        text_clean = re.sub("['\-+():.]",'',text_clean)
        text_clean = re.sub("[^a-z0-9]",' ',text_clean)
    
    json_response = {
    'status_code':200,
    'description':'teks sudah bersih',
    'data':text_clean,}
    
    return jsonify(json_response)
    
    
## Data Input
@swag_from("docs/input_csv.yml", methods=['POST'])
@app.route('/data_csv',methods=['POST'])
def data_input():
    if request.method == 'POST':
        file = request.files['file']
        
        try:
            data = pd.read_csv(file,encoding = 'iso-8859-1')
        except:
            data = pd.read_csv(file,encodingg = 'utf-8')
            
    for i in range(len(data)):
        text = data['Tweet'][i]
        text_clean = text.lower()
        text_clean = re.sub('user','',text_clean)
        text_clean = re.sub('rt :','',text_clean)
        text_clean = re.sub(r'^\n\n',' ',text_clean)
        text_clean = re.sub('\d.*.$','',text_clean)
        text_clean = re.sub('\A.*\\\\n',' ',text_clean)
        text_clean = re.sub(r'^\\x[0-9a-zA-Z]','',text_clean)
        text_clean = re.sub('\A.*https','',text_clean)
        text_clean = re.sub(' +',' ',text_clean)
        text_clean = re.sub("['\-+():.]",'',text_clean)
        text_clean = re.sub("[^a-z0-9]",' ',text_clean)
        
        database.execute("INSERT INTO data(id,text_old, text_cleaned) VALUES (?,?,?)",(i,text,text_clean))
        database.commit()

    json_response = {
    'status_code':200,
    'description':'teks sudah bersih',
    'data':text_clean,}
        
        
    return jsonify(json_response)
    
@app.errorhandler(400)
def handle_400_error(_error):
    "return sebuah http 400 error kepada client"
    return make_response(jsonify({'error':'Misunderstood'}),400)

@app.errorhandler(401)
def handle_401_error(_error):
    "return sebuah http 401 error kepada client"
    return make_response(jsonify({'error':'Unauthorized'}),401)

@app.errorhandler(404)
def handle_404_error(_error):
    "return sebuah http 404 error kepada client"
    return make_response(jsonify({'error':'Not Found'}),404)

@app.errorhandler(500)
def handle_500_error(_error):
    "return sebuah http 500 error kepada client"
    return make_response(jsonify({'error':'Server'}),500)

if __name__ == '__main__':
    app.run()


# In[ ]:




