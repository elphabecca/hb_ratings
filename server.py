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
    current_user_email = current_user[0].email
    current_user_pw = current_user[0].password

    # Current user is not yet in DB
    if current_user == []:

        # add the new user to database
        new_user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()

        # Sets session for current user
        session['current_user'] = email
        flash("Welcome new super-rater of super-movies. You're SUPER.")

        return redirect("/")

    # Current user is already in DB -- check for password verification    
    else:

        if password == current_user_pw:
            session['current_user'] = email
            flash("Welcome back!  You're logged in!")

            return redirect("/")

        else:
            flash("Wrong Password. Try again.")

            return redirect('/login')

@app.route('/login')
def login_form():
    """Display Login Form"""

    return render_template('login.html')


@app.route('/logout')
def logout_page():
    """Display logout page"""

    session['current_user'] = None
    flash("You've been successfully logged out.")

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)
