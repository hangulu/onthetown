"""
This module executes the Flask application.
"""

import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, json, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import Error
from db_init import create_connection

app = Flask(__name__, template_folder="static/templates")
app.secret_key = "DooLouGulu"
app.config['SESSION_TYPE'] = 'redis'
Session(app)


# Establish connection
conn = create_connection("server/users.db")

def get_preferences(email):
    """
    Given a user's email address, return their preferences.
    email (string): Email address of a user.

    return: A dictionary of preferences.
    """
    c = conn.cursor()
    # Extract the data
    serial_activity = c.execute("SELECT activity FROM prefs WHERE email = ?", (email, )).fetchone()[0]
    activity = serial_activity.split("\0")
    price = c.execute("SELECT price FROM prefs WHERE email = ?", (email, )).fetchone()[0]
    rating = c.execute("SELECT rating FROM prefs WHERE email = ?", (email, )).fetchone()[0]
    latitude = c.execute("SELECT latitude FROM prefs WHERE email = ?", (email, )).fetchone()[0]
    longitude = c.execute("SELECT longitude FROM prefs WHERE email = ?", (email, )).fetchone()[0]

    c.close()
    return {"activity": activity, "price": price, "rating": rating, "lat": latitude, "long": longitude}


@app.route("/")
def main():
    if "name" in session:
        return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)
    else:
        return render_template("index.html")

@app.route("/signup")
def sign_up():
    if "name" in session:
        return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)
    else:
        return render_template("signup.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if "name" in session:
        return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)
    else:
        if request.method == "POST":
            c =  conn.cursor()
            try:
                _name = request.form["inputName"]
                _email = request.form["inputEmail"]
                _password = request.form["inputPassword"]

                # Validate the input
                if _name and _email and _password:
                    hashed_password = generate_password_hash(_password)
                    statement = c.execute("SELECT email FROM users")
                    for row in statement.fetchall():
                        if _email in row[0]:
                            c.close()
                            return render_template("signup.html", error_msg="A user with this email address already exists. Please use another or sign in above.")
                    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (_name, _email, hashed_password))
                    c.execute("INSERT INTO prefs (email, activity, price, rating, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)", (_email, "bakery", 3, 3.0, 40.807835, -73.963957))
                    conn.commit()
                    c.close()
                    session["name"] = _name
                    session["email"] = _email
                    return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)
                else:
                    c.close()
                    return render_template("signup.html", error_msg="Please complete all required fields.")

            except Exception as e:
                return json.dumps({'error': str(e)})
            finally:
                c.close()
        else:
            return render_template("signup.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if "name" in session:
        return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)
    else:
        if request.method == "POST":
            c = conn.cursor()
            try:
                _email = request.form["inputEmail"]
                _password = request.form["inputPassword"]

                # Validate the input
                if _email and _password:
                    statement = c.execute("SELECT email FROM users")
                    for row in statement.fetchall():
                        if _email in row[0]:
                            pas = c.execute("SELECT password FROM users WHERE email = ?", (_email, ))
                            for words in pas.fetchone():
                                if check_password_hash(words, _password):
                                    _name = c.execute("SELECT name FROM users WHERE email = ?", (_email, )).fetchone()[0]
                                    session["name"] = _name
                                    session["email"] = _email
                                    return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)
                    c.close()
                    return render_template("login.html", error_msg="We were unable to find a match for these credentials. Please try again.")
                else:
                    render_template("login.html", error_msg="Please input valid credentials.")

            except Exception as e:
                return json.dumps({'error': str(e)})
            finally:
                c.close()
        else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("name", None)
    return render_template("index.html")

@app.route("/pref", methods=["POST", "GET"])
def log_prefs():
    if request.method == "POST":
        c =  conn.cursor()
        try:
            act_checklist = request.form.getlist("act_check")
            _activity_type = "\0".join(act_checklist)
            _price_pref = request.form.get("price_pref", None)
            _rating_pref = request.form.get("rating_pref", None)
            _lat_location = request.form.get("lat_location", None)
            _long_location = request.form.get("long_location", None)

            _email = session["email"]

            # Validate the input
            if _activity_type and _price_pref and _rating_pref and  _lat_location and _long_location:
                c.execute("UPDATE prefs SET activity = ?, price = ?, rating = ?, latitude = ?, longitude = ? WHERE email = ?", (_activity_type, _price_pref, _rating_pref, _lat_location, _long_location, _email))
                conn.commit()
                c.close()
                return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=True)
            else:
                c.close()
                return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)

        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            c.close()
    else:
        return render_template("dashboard.html", name=session["name"], prefs=get_preferences(session["email"]), recent_update=False)

@app.route("/setup", methods=["POST", "GET"])
def start_event():
    if request.method == "POST":
        c =  conn.cursor()
        try:
            named_gathering = request.form.get("name_event", None).replace(" ", "-")

            _email = session["email"]
            _name = session["name"].replace(" ", "").lower()
            custom_link = _name + "-" + named_gathering

            # Validate the input
            if named_gathering:
                users = [{"email": _email, "name": _name, "organizer": True}]
                return render_template("setup.html", name=session["name"], named_gathering=named_gathering, link=custom_link, users=users)
            else:
                c.close()
                return render_template("setup.html", name=session["name"])

        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            c.close()
    else:
        return render_template("setup.html", name=session["name"])

@app.route("/plan/<c_link>", methods=["POST", "GET"])
def plan_event(c_link):
    if request.method == "POST":
        c =  conn.cursor()
        try:
            custom_link = c_link
            named_gathering = c_link.split("-")[1]

            _email = session["email"]
            _name = session["name"]
            _organizer = True

            # Validate the input
            if custom_link:
                db_name = custom_link.replace("-", "")
                create_query = "CREATE TABLE IF NOT EXISTS {} (email TEXT PRIMARY KEY, name TEXT, organizer BOOLEAN)".format(db_name)
                upsert_query = "REPLACE INTO {} (email, name, organizer) VALUES (?, ?, ?)".format(db_name)
                c.execute(create_query)
                c.execute(upsert_query, (_email, _name, _organizer))
                return render_template("setup.html", name=session["name"], named_gathering=named_gathering, link=custom_link)
            else:
                c.close()
                return json.dumps({'error': str("not working")})
                return render_template("setup.html", name=session["name"])

        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            c.close()
    else:
        return render_template("setup.html", name=session["name"])

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5002)
