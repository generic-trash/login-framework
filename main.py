from flask import *
from flask_json import *

app = Flask("login")
FlaskJSON(app)


@app.post("/login")
@as_json
def login():
    data = request.get_json()


