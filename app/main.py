import os, requests 
from flask import Flask, json, jsonify, request
from dotenv import load_dotenv # har samma funktion som dotenv i Node.js dvs. automatiskt laddar env variablerna hit 

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.query import Query

load_dotenv()  # Load variables from .env

app = Flask(__name__)  # Instansierar Flask applikationen , _name__ = namnet på skriptet vi kör, kallas "dunder" 
app.config['JSON_AS_ASCII'] = False     # Tillåt utf-8 i JSON

# Konfiguration för SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DBB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)   # Skapar databas instans


# todo Ändra så att token kommer från electron
cabins_token = os.environ.get('CABINS_TOKEN')


#Service datamodell
class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    orders = db.relationship('Order', backref='services')
    cabin_id = db.Column(db.String())

    def __refr__(self):
        return '<Services {}>'.format(self.service)

#Order datamodell 
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime())
    services_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    cabin_id = db.Column(db.String())

    def __refr__(self):
        return '<Orders {}>'.format(self.id)


# Default route to / app
@app.route("/", methods = ['GET'])
def index():
    if request.method == 'GET':
        return 'Stugunderhållstjänsten'


# Få en  order by ID
@app.route("/orders/<int:id>", methods = ['GET'])
def cab(id):
    ret = []
    if request.method == 'GET':
        #User.query.filter_by(username='peter')
        order_to_show = Order.query.get(id)
        try:
            ret.append({
            'cabinID': order_to_show.cabin_id,
            'serviceID': order_to_show.services_id
            })
        except:
            ret = ["error"]

    return jsonify(ret)

# Få och skapa bokningar
@app.route("/orders", methods = ['GET', 'POST'])
def orders():
    ret = [] 

    if request.method == 'GET':
        # Loopa varje rad i service-tabellen och lägg till i ret
        for o in Order.query.all():
            ret.append({ 
                'id': o.id,
                'order_date': o.order_date, 
                'services_id': o.services_id,
                'cabin_id': o.cabin_id 
                })

    if request.method == 'POST':
        try:
            body = request.get_json()

            new_order = Order(
                order_date=body['order_date'],
                services_id = body['services_id'],
                cabin_id = body['cabin_id'])
            db.session.add(new_order)
            db.session.commit()

            ret = ["Added an order for the chosen service!"]
        except:
            return "There was an error ordering!"


    return jsonify(ret)



#Ändra eller radera en viss bokning
@app.route("/orders/<int:id>", methods=['DELETE', 'PUT'])
def getOrderById(id):
    if request.method == 'DELETE':
        order_to_delete = Order.query.get(id)

        try: 
            db.session.delete(order_to_delete)
            db.session.commit()
            return 'You just deleted an order'

        except:
            return "There was an error deleting"

    if request.method == 'PUT':
        order_to_update = Order.query.get(id)
        body = request.get_json()

        try:
            order_to_update.order_date = body['order_date']
            db.session.commit()
            return 'You just updated an order'

        except:
            return 'There was an error editing the order'


#Hämta användarens stugor från Projekt 1 
@app.route("/cabins")
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
def services():
    ret = [] 

    if request.method == 'GET':
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