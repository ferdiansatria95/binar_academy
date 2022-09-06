import re
from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


app = Flask(__name__)

app.json_encoder= LazyJSONEncoder
swagger_template = dict(
info ={
    'title':LazyString(lambda: 'API Documentation for data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk data preprocessing dan modelling'),
},
    host = LazyString(lambda:request.host)    
)

swagger_config ={
    "headers":[],
    "specs": [
        {
            "endpoint":'docs',
            "route" : '/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui":True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)
@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response ={
        'status_code' :200,
        'description' :"Menyapa Hello world",
        'data' : "Hello World",
    }
    
    response_data =jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()   