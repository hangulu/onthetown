"""
This module executes the Flask application.
"""

import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, json, request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import Error
from db_init import create_connection

app = Flask(__name__, template_folder="static/templates")

# Establish connection
conn = create_connection("server/users.db")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/register", methods=["POST", "GET"])
def register():
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
                conn.commit()
                c.close()
                return render_template("dashboard.html")
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
                                return render_template("dashboard.html")
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

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5002)
