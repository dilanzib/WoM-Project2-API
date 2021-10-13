import os, requests 
from flask import Flask, json, jsonify, request
from dotenv import load_dotenv # har samma funktion som dotenv i Node.js dvs. automatiskt laddar env variablerna hit 

from flask_sqlalchemy import SQLAlchemy

load_dotenv()  # Load variables from .env

app = Flask(__name__)  # Instansierar Flask applikationen , _name__ = namnet på skriptet vi kör, kallas "dunder" 
app.config['JSON_AS_ASCII'] = False     # Tillåt utf-8 i JSON

# Konfiguration för SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)   # Skapar databas instans


# TODO: Ändra så att token kommer från electron
cabins_token = os.environ.get('CABINS_TOKEN')


#Service datamodell
class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())

    def __refr__(self):
        return '<Services {}>'.format(self.service)



# Skapar automatiskt en inlogging till användaren "test@gmail.com" och ger ut en token när man kör Flask run 
# men vi vill få den från front-enden. Sparar ändå koden i fall
# den kan användas för att få en ny kod jwt till testning2

'''
try:
    url = 'https://wom-project1.azurewebsites.net/users/login'  
    header = { 'Content-Type': 'application/json' }
    body = {  "email": "test@gmail.com",  "password": os.environ.get('CABINS_PASSWORD')}

    response = requests.post(url, headers=header, json=body)

    cabins_token = response.content.decode('utf-8')
    print("Token: {}".format(response.content.decode('utf-8')))

except Exception as e:
    print(e)
'''


#Hämta användarens stugor från Projekt 1 
@app.route("/cabins/owned")
def cabins():
    print("GET My cabins")
    url = 'https://wom-project1.azurewebsites.net/cabins/owned'
    print(request.headers)
    # todo: hämta jwt från request i stället
    token = request.headers['Authorization']
    header = { 'Authorization': 'Bearer {}'.format(token) }
    
    response = requests.get(url, headers=header)
    
    return jsonify(response.json())




# Hämta och skapa services
@app.route("/services", methods = ['GET', 'POST'])
def index():
    ret = [] 

    if request.method == 'GET':
        # Loopa varje rad i service-tabellen och lägg till i ret
        for s in Services.query.all():
            ret.append({ 
                'id': s.id,
                'service': s.service, 
                'updated_at': s.updated_at 
                })
        
    if request.method == 'POST':
        body = request.get_json()

        new_service = Services(service=body['service'])
        db.session.add(new_service)
        db.session.commit()

        ret = ["Added a new service "]

    return jsonify(ret)



# Ändra och radera services med ID
@app.route("/services/<int:id>", methods=['DELETE', 'PUT'])
def getServiceById(id):

    if request.method == 'DELETE':
        service_to_delete = Services.query.get(id)

        try: 
            db.session.delete(service_to_delete)
            db.session.commit()
            return 'You just deleted an service'

        except:
            return "There was an error deleting"

    if request.method == 'PUT':
        service_to_update = Services.query.get(id)
        body = request.get_json()

        try:
            service_to_update.service = body['service']
            db.session.commit()
            return 'You just updated an service'

        except:
            return 'There was an error updatig the service '





# Run app if it's called directly
if __name__ == "__main__":
          app.run()