import os, requests 
from flask import Flask, jsonify, request
from dotenv import load_dotenv # har samma funktion som dotenv i Node.js dvs. automatiskt laddar env variablerna hit 

from flask_sqlalchemy import SQLAlchemy

# Load variables from .env
load_dotenv()
print(os.environ.get('HELLO')) 

def get_notes():
    return [{ "test": "fää" }, {"test": "bar" }]


# Instansierar Flask applikationen , _name__ = namnet på skriptet vi kör, kallas "dunder" 
app = Flask(__name__)
# Tillåt utf-8 i JSON
app.config['JSON_AS_ASCII'] = False

# Konfiguration för SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)   # Skapar databas instans

# User = en databasmodell 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())

    def __refr__(self):
        return '<User {}>'.format(self.email)

# @ = en decorator, det är en skild funktion som denhär funktionen kör igenom
@app.route("/", methods = ['GET', 'POST', 'PUT'])
def index():
    ret = [] 
    if request.method == 'GET':
        # Loopa varje rad i User-tabellen och lägg till i ret
        for u in User.query.all():
            ret.append({'id': u.id, 'email': u.email, 'updated_at': u.updated_at})

    if request.method == 'POST':
        body = request.get_json()

        new_user = User(email=body['email'])
        db.session.add(new_user)
        db.session.commit()

        ret = ["Added new user "]

    if request.method == 'PUT':
        ret = [ " put " ]

    return jsonify(ret)



@app.route("/notes")
def notes():
    print("GET notes")

    return jsonify(get_notes())









# Run app if called directly
if __name__ == "__main__":
          app.run()