import service
import json
import hashlib
import datetime
import re
import os
from flask import Flask, request, jsonify, session, render_template, redirect

template_dir = os.path.abspath("../Frondend")
print(template_dir)
app = Flask(__name__, template_folder=template_dir, static_folder=template_dir, static_url_path="/static/")
app.secret_key = "OSP_SECRET_KEY::TODO:CHANGE!"

active_users = {}  # key: session_id, value: user_id


def get_user_id_from_session(session: dict) -> str:
    try:
        session_id = session["session_id"]
        return active_users[session_id]
    except Exception as e:
        print(f"Exception in get_user_id_from_session: {e}")
        return ""


def hash_pw(unhashed_pw: str) -> str:
    return hashlib.sha256(unhashed_pw.encode("utf-8")).hexdigest()


@app.route("/", methods=["GET"])
def login_page():
    return render_template('loginPage/loginPage.html')


@app.route("/login", methods=["POST"])
def login():
    content = request.json
    
    email = content["email"]
    passwd = content["passwd"]
    
    user = json.loads(service.user_get(email=email, passwd=hash_pw(passwd)))

    if user != None:
        unencoded_session_id = user.id + str(datetime.datetime.now())
        session_id = hashlib.sha256(unencoded_session_id.encode("utf-8")).hexdigest()
        session["session_id"] = session_id
        active_users[session_id] = user["id"]
        
        return {}, 200
    
    return {}, 404  # error_msg="Nutzername oder Passwort falsch"


# Registration will be a Pop-Up on the Login-Page,
# therefore a GET to render a register-page will not be necessary
@app.route("/register", methods=["POST"])
def register():
    content = request.json
    
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    passwd = content["passwd"]
    gender = content["gender"]
    age = content["age"]
    city = content["city"]
    
    errors = 0
    msg = ""
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors += 1
        msg += "Die E-Mail-Adresse ist nicht valide\r\n"
        
    try:
        gender = int(gender)
    except:
        errors += 1
        msg += "Gender hat keinen validen Wert\r\n"
        
    try:
        age = int(age)
    except:
        errors += 1
        msg += "Alter hat keinen validen Wert\r\n"
        
    if errors > 0:
        print("Error registering User: {msg}")
        return {}, 404
    
    # No clear pass on the db!
    passwd = hash_pw(passwd)
    
    user = json.loads(service.user_create(first_name, last_name, email, passwd, gender, age, city))
    if user != None:
        unencoded_session_id = user["id"] + str(datetime.datetime.now())
        session_id = hashlib.sha256(unencoded_session_id.encode("utf-8")).hexdigest()
        session["session_id"] = session_id
        active_users[session_id] = user["id"]
        
        return {}, 200
    
    return {}, 404  # error_msg="Etwas ist schief gegangen, bitte Informieren sie den Support."


@app.route("/home/", methods=["GET"])
def home_page():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    # send all upcoming appointments to the site, as this is the standard-view/-tab
    appointments = service.apt_get(user_id=user_id)
    if len(appointments) > 1:
        appointments = sorted(appointments, reverse=True, key= lambda apt: apt["date"])
    
    return render_template("upcoming/upcoming.html", data={"appointments": appointments}), 200


# Settings will be a Pop-Up/Slide-In on the homepage
# therefore a GET to render a settings-page will not be necessary
@app.route("/api/user/", methods=["PUT"])
def change_profile():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    user = json.loads(service.user_get(id=user_id))
    if user == None:
        return {}, 401
    
    user_info = user
    
    content = request.json
    
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    passwd = content["passwd"]
    gender = content["gender"]
    age = content["age"]
    city = content["city"]
    
    errors = 0
    msg = ""
    
    if user_info["passwd"] == hash_pw(passwd):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors += 1
            msg += "Die E-Mail-Adresse ist nicht valide\r\n"
            
        try:
            gender = int(gender)
        except:
            errors += 1
            msg += "Gender hat keinen validen Wert\r\n"
            
        try:
            age = int(age)
        except:
            errors += 1
            msg += "Alter hat keinen validen Wert\r\n"
    else:
        errors += 1
        msg = "Passwort Falsch"
        
    if errors > 0:
        return {}, 404
    
    # changing email or password is currently not allowed
    service.user_update(user_id, first_name, last_name, user_info["email"], user_info["passwd"], gender, age, city)
    
    return {}, 200


@app.route("/api/Friendzone/", methods=["GET"])
@app.route("/api/Friendzone/<string:fz_id>", methods=["GET"])
def fz_get(fz_id=""):
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return service.fz_get(user_id, fz_id), 200


@app.route("/api/Appointment/", methods=["GET"])
@app.route("/api/Appointment/<string:apt_id>", methods=["GET"])
def apt_get(apt_id=""):
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return service.apt_get(user_id, apt_id), 200


@app.route("/api/Comment/", methods=["GET"])
@app.route("/api/Comment/<string:apt_id>", methods=["GET"])
def comment_get(apt_id=""):
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return service.comment_get(user_id, apt_id), 200


if __name__ == "__main__":
    app.run()