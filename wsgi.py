# Python skript som startar upp appen, denhär e den Heroku vill använda
from app.main import app
  
if __name__ == "__main__":
        app.run()