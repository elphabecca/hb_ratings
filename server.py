"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_form():
    """Form for registering a new user."""

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def show_form_results():
    """Process the form that the user submitted"""

    # results from form
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    email = request.form.get("email")
    password = request.form.get("password")

    current_user = User.query.filter_by(email=email).all()
    print current_user

    if current_user == []:

        # add the new user to database
        new_user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()

        flash("Welcome new super-rater of super-movies. You're SUPER.")
        print "\n\n\n\nTHIS USER IS NEW %s is IN THE DATABASE???\n\n\n\n" % new_user
        return redirect("/")
    else:
        flash("Welcome back!  You're logged in!")
        print "\n\n\n\nTHIS USER IS IN\n\n\n\n"
        return redirect("/")

@app.route('/login')
def login_form():
    """Display Login Form"""

    return render_template('login.html')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)
