from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
from storage import storage

app = Flask(__name__)
CORS(app)





if __name__ == "__main__":
    app.run(debug=True, port=8000)
