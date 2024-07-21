from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message 
import random
import string

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, Promptapp!"

if __name__ == '__main__':
    app.run(debug=True)