# WoM-Project2
Underhållsstjänst för stugor

The files Procfile, wsgi.py and runtime.txt contain all the info Heroku needs to run the app.


pip = Pythons package manager  (npm = är Nodes package manager)
pip freeze = allt de vi har installerat 
pip freeze > requirements.txt 
—> Skriv outputet från föregående kommando till denhär filen  (i dehär fallet från freeze till requirements.txt filen)

pip install -r requirements.txt   --> Installera allt de vi har i requirements.txt

När man gör Flask , använder man funktionen Jsonify


Del1.  Få en lista på de stugor en användare själv äger
Del2.  Information av olika tjänster och beställning av dem    
          /orders       /services 

Del3. Integrationsbit: en request som gör en andrahands request till Projekt1.
Om man in den nya APIn kör GET /cabins med en giltig JWT token, så gör den en ny request till projekt1/cabins/owned och visar det innehållet.

Del4. Front end till appen: Desktop app —> Electron.js
