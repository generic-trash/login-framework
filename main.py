from flask import *
from flask_json import *
from userdb import *
from sessionmanager import *

userdb = UserDB()
sessionman = SessionManager()
app = Flask("login", static_folder='static', static_url_path='')
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
        print(data)
        return jsonify(status=400, description="All Information not Provided")
    if data["password"] != data["confirm"]:
        return jsonify(status=400, description="Passwords do not match")
    status = userdb.add_user(data["username"], data["email"], data["password"])
    if status["status"] == 200:
        tok = sessionman.create_session_for_user(data["username"])
        resp = jsonify(status=200, authtoken=tok)
        resp.set_cookie("onionauth", tok)
        return resp
    return jsonify(status)


@app.post("/logout")
def logout():
    resp = jsonify(status=200)

    if "onionauth" in request.cookies:
        sessionman.delete_session(request.cookies["onionauth"])
        resp.delete_cookie("onionauth")
    return resp


@app.get("/users/<username>/publicdata")
@as_json
def get_publicdata1(username):
    return userdb.get_public_data(username)

@app.get("/whoami")
@as_json
def get_whoami():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=200, unauthenticated=True)
    else:
        return dict(status=200, unauthenticated=False, username=sessionman.get_session(request.cookies["onionauth"]))
@app.get("/me/publicdata")
@as_json
def get_publicdata():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot access my publicdata if unauthenticated")

    return userdb.get_public_data(sessionman.get_session(request.cookies["onionauth"]))


@app.post("/me/publicdata")
@as_json
def set_publicdata():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set public data if unauthenticated")
    data = request.get_json()
    return userdb.set_public_data(sessionman.get_session(request.cookies["onionauth"]), data)


@app.route("/me/publicdata", methods=["UPDATE"])
@as_json
def update_publicdata():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set public data if unauthenticated")
    data = request.get_json()
    return userdb.update_public_data(sessionman.get_session(request.cookies["onionauth"]), data)


@app.route("/me/privatedata", methods=["UPDATE"])
@as_json
def update_privatedata():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set private data if unauthenticated")
    data = request.get_json()
    return userdb.update_public_data(sessionman.get_session(request.cookies["onionauth"]), data)


@app.get("/me/privatedata")
@as_json
def get_privatedata():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot access private data if unauthenticated")

    return userdb.get_private_data(sessionman.get_session(request.cookies["onionauth"]))


@app.post("/me/privatedata")
@as_json
def set_privatedata():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot set private data if unauthenticated")
    data = request.get_json()
    return userdb.set_private_data(sessionman.get_session(request.cookies["onionauth"]), data)


@app.get("/me/email")
@as_json
def get_email():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot get email if unauthenticated")
    return userdb.get_email(sessionman.get_session(request.cookies["onionauth"]))


@app.post("/me/email")
@as_json
def set_email():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot get email if unauthenticated")
    data = request.get_json()
    if "email" not in data:
        return dict(status=400, description="No Email Provided")
    return userdb.set_email(sessionman.get_session(request.cookies["onionauth"]), data["email"])


@app.post("/changepassword")
@as_json
def change_password():
    if "onionauth" not in request.cookies or not sessionman.get_session(request.cookies["onionauth"]):
        return dict(status=401, description="Cannot change password if unauthenticated")
    data = request.get_json()
    if any([x not in data for x in ["current", "password", "confirm"]]):
        return dict(status=400, description="All Information not Provided")
    if data["password"] != data["confirm"]:
        return jsonify(status=400, description="Passwords do not match")
    if not userdb.check_pass(sessionman.get_session(request.cookies["onionauth"]), data["current"]):
        return dict(status=401, description="Old Password is Incorrect")

    data = request.get_json()
    return userdb.set_password(sessionman.get_session(request.cookies["onionauth"]), data["password"])


if __name__ == "__main__":
    app.run()
