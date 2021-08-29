# Import what we need from flask
from flask import Flask
from flask import jsonify

# Create a Flask app inside `app`
app = Flask(__name__)

# Assign a function to be called when the path `/` is requested
@app.route("/")
def index():
    return "hello world"


@app.route("/cow")
def cow():
    return "MOoooOo!"
