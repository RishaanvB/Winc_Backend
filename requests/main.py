__winc_id__ = "cc1b724762854e85a8defa04287f708b"
__human_name__ = "requests"


from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Home, sweet home.</p>"


@app.route("/greet/")
@app.route("/greet/<example_name>")
def greet(example_name="world"):
    return f"<h1>Hello, {example_name}!</h1>"
