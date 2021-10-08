import os   # bibliotek som innehåller många funktioner för att kunna kommunicera med datorns operativsystem
from flask import Flask, jsonify  
from dotenv import load_dotenv # har samma funktion som dotenv i Node.js dvs. automatiskt laddar env variablerna hit 

# Load variables from .env
load_dotenv()
print(os.environ.get('HELLO')) 

def get_notes():
    return [
        { "test": "fää" }, 
        {"test": "bar" }
    ]

# Instansierar Flask applikationen , _name__ = namnet på skriptet vi kör, kallas "dunder" 
app = Flask(__name__)
# Tillåt utf-8 i JSON
app.config['JSON_AS_ASCII'] = False

# @ = en decorator, det är en skild funktion som denhär funktionen kör igenom
@app.route("/")
def index():  
    return "Hello Flask!"



@app.route("/notes")
def notes():
    print("GET notes")

    return jsonify(get_notes())









# Run app if called directly
if __name__ == "__main__":
          app.run()