from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Promptapp!"

if __name__ == '__main__':
    app.run(debug=True)