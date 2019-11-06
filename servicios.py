import os
from flask import Flask, flash, request, redirect, url_for, session,jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import guardar as prime
from DiagnosticoBases import diagnosticar as diagnostico




logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')


"""
LAS EXTENSIONES DE LOS ARCHIVOS QUE SON PERMITIDOS
"""
UPLOAD_FOLDER = './PruebaSubida'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

@app.route('/')
def hola():
    return "hola mundo"

# Recibe el archivo en formato base64 para proceder a reconstrir el archivo  
@app.route('/enviar', methods=['POST'])
def enviar():
    
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    logger.info(""+destination)
    temp=""+destination    
    fileExtension= os.path.splitext(temp)[1]
    prime.enviar(destination,filename)
    if(fileExtension=='.xlsx'):
       return jsonify(diagnostico(destination))
    else:
        return jsonify({'Estado':'No Excel'})


@app.route('/login', methods=['PUT'])
def login():
    content = request.get_json()
    email = content['email']
    password = content['password']
    #Campos email - Password HACER MATCH CON LA DB Y QUE RETORNE ESTADO SUCCESS O FAIL
    return jsonify({'Estado':'Success'})
 

@app.route('/register', methods=['POST'])
def register():
    content = request.get_json()
    name = content['name']
    departamento = content['departamento']
    email = content['email']
    password = content['password']
    nit = content['nit']
    representante = content['representante']
    cluster = content['cluster']
    cellphone = content['cellphone']
    

    #Si la escritura en la db no falla por columnas repetidas como email , retornar Success
    return jsonify({'Estado':'Success'})
  
    
    
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(threaded=True,host='0.0.0.0',debug=False,port=int("5000"))
