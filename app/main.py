import os
from flask import Flask
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
print(os.environ.get('HELLO'))

# Create Flask instance
app = Flask(__name__)

# Default route to /
@app.route("/")
def index():
    return "Hello Flask!"

# Run app if called directly
if __name__ == "__main__":
        app.run()