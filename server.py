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

@app.route("/movies")
def movie_list():
    """Show a list of movies"""

    movies = db.session.query(Movie.movie_id, Movie.movie_title).order_by(Movie.movie_title).all()

    # movies = Movie.query.order_by(Movie.movie_title).all()
    return render_template("movie_list.html", movies=movies)

@app.route("/movie/<int:id>", methods = ["POST", "GET"])
def display_movie(id):
    """Displays information about the movie"""

    # Unlike the display_user function where a_user var returns a list of objects,
    # the display_movie function's user_rating var returns a list of tuples. B/c learning
    user_rating = db.session.query(Rating.score, Rating.user_id).filter_by(movie_id = id).all()
    movie_title = db.session.query(Movie.movie_title).filter_by(movie_id = id).one()
    movie_title = str(movie_title[0])

    if request.method == "POST":
        user_score = request.form["score"]
        new_user_id = db.session.query(User.user_id).filter_by(email = session["login"]).one()
        new_rating = Rating(movie_id=id, user_id = new_user_id[0], score = user_score)
        db.session.add(new_rating)
        db.session.commit()
        flash("Thank you for rating this movie.")
        return redirect("/movie/"+str(id))


    return render_template("movie_info.html", user_rating = user_rating, 
                            movie_title=movie_title, movie_id = id)



@app.route("/login", methods = ["POST", "GET"])
def login_form():
    """Show login form as a separate page"""

    if request.method == "POST":
        username = request.form["username_input"]
        password = request.form["password_input"]
        user_object = User.query.filter(User.email == username).first()
        
        if user_object:
            if user_object.password == password:
                session["login"] = username
                flash("You logged in successfully")
                return redirect("/")
            else:
                flash("Incorrect password. Try again.")
                return redirect("/login")
        else:
            flash("We do not have this email on file. Click Register if you would like to create an account.")
            return redirect("/login")

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

        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]
        zipcode = request.form["zipcode"]

        if User.query.filter(User.email == email).first():
            flash("It looks like you've already registered with that email. Try again.")
            return redirect("/register")
        else:
            new_user = User(email = email, password = password,
                            age = age, zipcode = zipcode)
            db.session.add(new_user)
            db.session.commit()
            flash("Thanks for creating an account with the Judgemental Eye!")
            return redirect("/")

    return render_template("registration_form.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()