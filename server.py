"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show a list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/user/<int:id>")
def display_user(id):
    """Displays information about the user."""

    a_user = User.query.get(id)

    return render_template("user_info.html", a_user = a_user)


@app.route("/login", methods = ["POST", "GET"])
def login_form():
    """Show login form as a separate page"""

    if request.method == "POST":
        username = request.form["username_input"]
        password = request.form["password_input"]
        session["login"] = session.setdefault("login", [username])
        flash("You logged in successfully")
        print "logged in", session
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout_button():
    """Remove login information from session"""

    session.pop("login")
    flash("You've successfully logged out. Goodbye.")
    print "logged out", session
    return redirect("/")

@app.route("/register", methods = ["POST", "GET"])
def register_user():
    """Collect registration data from user"""

    if request.method == "POST":
        pass

    return render_template("registration_form.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()