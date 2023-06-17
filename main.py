from flask import *
from flask_json import *
from userdb import *
from sessionmanager import *

userdb = UserDB()
sessionman = SessionManager()
app = Flask("login")
FlaskJSON(app)


@app.post("/login")
def login():
    data = request.get_json()
    if "username" not in data or "password" not in data:
        return jsonify(status=400, description="Username or Password Not Provided")
    if not userdb.check_pass(data["username"], data["password"]):
        return jsonify(status=401, description="Username or Password is Incorrect")
    tok = sessionman.create_session_for_user(data["username"])
    resp = jsonify(status=200, authtoken=tok)
    resp.set_cookie("onionauth", tok)
    return resp


@app.post("/register")
def register():
    data = request.get_json()
    if any([x not in data for x in ["username", "password", "confirm", "email"]]):
        return jsonify(status=400, description="All Information not Provided")
    if not userdb.check_pass(data["username"], data["password"]):
        return jsonify(status=401, description="Username or Password is Incorrect")
    tok = sessionman.create_session_for_user(data["username"])
    resp = jsonify(status=200, authtoken=tok)
    resp.set_cookie("onionauth", tok)


@app.post("/logout")
def logout():
    resp = jsonify(status=200)

    if "onionauth" in request.cookies:
        sessionman.delete_session(request.cookies["onionauth"])
        resp.delete_cookie("onionauth")
    return resp


@app.get("/users/<username>/publicdata")
@as_json
def get_publicdata(username):
    return userdb.get_public_data(username)


@app.get("/me/publicdata")
@as_json
def get_publicdata():
    if "onionauth" not in request.cookies or sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot access my publicdata if unauthenticated")

    return userdb.get_public_data(sessionman.get_session(request.cookies["onionauth"]))


@app.post("/me/publicdata")
@as_json
def set_publicdata():
    if "onionauth" not in request.cookies or sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set public data if unauthenticated")
    data = request.get_json()
    return userdb.set_public_data(sessionman.get_session(request.cookies["onionauth"]), data)


@app.route("/me/publicdata", methods=["UPDATE"])
@as_json
def update_publicdata():
    if "onionauth" not in request.cookies or sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set public data if unauthenticated")
    data = request.get_json()
    return userdb.update_public_data(sessionman.get_session(request.cookies["onionauth"]), data)


@app.route("/me/privatedata", methods=["UPDATE"])
@as_json
def update_privatedata():
    if "onionauth" not in request.cookies or sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set private data if unauthenticated")
    data = request.get_json()
    return userdb.update_public_data(sessionman.get_session(request.cookies["onionauth"]), data)


@app.get("/me/privatedata")
@as_json
def get_privatedata():
    if "onionauth" not in request.cookies or sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot access private data if unauthenticated")

    return userdb.get_private_data(sessionman.get_session(request.cookies["onionauth"]))


@app.post("/me/privatedata")
@as_json
def set_privatedata():
    if "onionauth" not in request.cookies or sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set private data if unauthenticated")
    data = request.get_json()
    return userdb.set_private_data(sessionman.get_session(request.cookies["onionauth"]), data)


if __name__ == "__main__":
    app.run()
