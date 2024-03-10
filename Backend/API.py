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


@app.route("/login/", methods=["POST"])
def login():
    content = request.json
    
    try:
        email = content["email"]
        passwd = content["passwd"]
    except:
        return {}, 404
    
    user = json.loads(service.user_get(email=email, passwd=hash_pw(passwd)))

    if user != None and type(user) != list:
        unencoded_session_id = str(user["id"]) + str(datetime.datetime.now())
        session_id = hashlib.sha256(unencoded_session_id.encode("utf-8")).hexdigest()
        session["session_id"] = session_id
        active_users[session_id] = user["id"]
        
        return {}, 200
    
    return {}, 404  # error_msg="Nutzername oder Passwort falsch"


# Registration will be a Pop-Up on the Login-Page,
# therefore a GET to render a register-page will not be necessary
@app.route("/register/", methods=["POST"])
def register():
    content = request.json
    
    try:
        first_name = content["first_name"]
        last_name = content["last_name"]
        email = content["email"]
        passwd = content["passwd"]
        age = content["age"]
        city = content["city"]
    except:
        return {}, 404
    
    errors = 0
    msg = ""
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors += 1
        msg += "Die E-Mail-Adresse ist nicht valide\r\n"
    else:
        email_user = json.loads(service.user_get(email=email))
        
        print(type(email_user))
        
        if type(email_user) != list and email_user != None:
            errors += 1
            msg += "Email schon vergeben\r\n"
        
    try:
        age = int(age)
    except:
        errors += 1
        msg += "Alter hat keinen validen Wert\r\n"
        
    if errors > 0:
        print(f"Error registering User: {msg}")
        return {}, 404
    
    # No clear pass on the db!
    passwd = hash_pw(passwd)
    
    user = json.loads(service.user_create(first_name, last_name, email, passwd, age, city))
    if user != None:
        unencoded_session_id = str(user["id"]) + str(datetime.datetime.now())
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
    appointments = json.loads(service.apt_get(user_id=user_id))
    
    if len(appointments) > 1:
        appointments = sorted(appointments, reverse=True, key= lambda apt: apt["date"])
    
    return render_template("upcomingsEvents/upcomingsEvents.html", data={"appointments": appointments}), 200


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
    
    try:
        first_name = content["first_name"]
        last_name = content["last_name"]
        email = content["email"]
        passwd = content["passwd"]
        age = content["age"]
        city = content["city"]
    except:
        return {}, 404
    
    errors = 0
    msg = ""
    
    if user_info["passwd"] == hash_pw(passwd):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors += 1
            msg += "Die E-Mail-Adresse ist nicht valide\r\n"

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
    service.user_update(user_id, first_name, last_name, user_info["email"], user_info["passwd"], age, city)
    
    return {}, 200


@app.route("/api/friendzone/", methods=["GET"])
@app.route("/api/friendzone/<string:fz_id>", methods=["GET"])
def fz_get(fz_id=""):
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return service.fz_get(user_id, fz_id), 200


@app.route("/api/friendzone/", methods=["POST"])
def fz_create():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    content = request.json
    
    try:
        name = content["name"]
    except:
        return {}, 404
    
    return service.fz_create(user_id=user_id, name=name), 200


@app.route("/api/appointment/", methods=["GET"])
@app.route("/api/appointment/<string:apt_id>", methods=["GET"])
def apt_get(apt_id=""):
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return service.apt_get(user_id, apt_id), 200


@app.route("/api/appointment/", methods=["POST"])
def apt_create():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    content = request.json
    
    try:
        user_id = content["user_id"]
        name = content["name"]
        date = content["date"]
        time_start = content["time_start"]
        time_stop = content["time_stop"]
        citycode = content["citycode"]
        city = content["city"]
        maxUser = content["maxUser"]
        notice = content["notice"]
        friendzone_id = content["friendzone_id"]
    except:
        return {}, 404
    
    return service.apt_create(user_id = user_id, name = name, date = date, time_start = time_start, time_stop = time_stop, citycode = citycode, city = city, maxUser = maxUser, notice = notice, friendzone_id = friendzone_id), 200


@app.route("/api/comment/", methods=["GET"])
@app.route("/api/comment/<string:apt_id>", methods=["GET"])
def comment_get(apt_id=""):
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return service.comment_get(user_id, apt_id), 200


@app.route("/api/comment/", methods=["POST"])
def comment_create():
    user_id = get_user_id_from_session(session)
    
    if user_id != "":
        return {}, 401
    
    content = request.json
    
    try:
        user_id = content["user_id"]
        apt_id = content["apt_id"]
        timestamp = content["timestamp"]
        comment_value = content["comment_value"]
    except:
        return {}, 404
    
    return service.comment_create(user_id=user_id, apt_id=apt_id, timestamp=timestamp, comment_value=comment_value), 200   


@app.route("/home/create/event/")
def create_apt_page():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return render_template("createEvent/createEvent.html"), 200


@app.route("/home/friendzone/")
def create_fz_page():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return render_template("friendzone/friendzone.html"), 200


@app.route("/impressum/")
def impressum_page():
    return render_template("legalNotice/legalNotice.html"), 200


@app.route("/datenschutz/")
def datenschutz_page():    
    return render_template("dataProtection/dataProtection.html"), 200


@app.route("/home/profile/")
def profile_page():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return render_template("userInfo/userInfo.html"), 200


@app.route("/home/requests/")
def requests_page():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return render_template("overview/overview.html"), 200

@app.route("/home/upcomingEvents/")
def upcoming_page():
    user_id = get_user_id_from_session(session)
    
    if user_id == "":
        return {}, 401
    
    return render_template("upcomingEvents/upcomingEvents.html"), 200


if __name__ == "__main__":
    app.run()