"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session, url_for
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


@app.route('/movies')
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", movies=movies)


@app.route('/movies/<int:movie_id>')
def show_movie_detail(movie_id):
    """Shows movie details."""

    curr_movie = Movie.query.get(movie_id)
    list_o_ratings = curr_movie.ratings
    
    # Math to find average rating
    sum_ratings = 0
    for rating in list_o_ratings:
        sum_ratings += rating.score
    avg_rating = float(sum_ratings/len(list_o_ratings))

    # logic for if user is logged in and rating flow
    if session['current_user'] is not None:
        user_id = session['current_user']
        movie_id = movie_id
        curr_user = User.query.get(user_id)
        curr_rating = Rating.query.filter_by(movie_id=movie_id, user_id=user_id).all()
        print "\n\n\n", curr_rating
        if curr_rating == []:
            # they don't have a rating for this movie
            print "cheese"
        else:
            curr_score = curr_rating[0].score
 
    return render_template("movie_detail.html",
                           list_o_ratings=list_o_ratings,
                           curr_movie=curr_movie,
                           avg_rating=avg_rating,
                           curr_score=curr_score)


@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Shows user details."""
    
    curr_user = User.query.get(user_id)

    age = curr_user.age
    zipcode = curr_user.zipcode
    list_o_ratings = curr_user.ratings

    return render_template('user_detail.html',
                           user_id=user_id,
                           age=age,
                           zipcode=zipcode,
                           list_o_ratings=list_o_ratings)

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

    # Current user is not yet in DB
    if current_user == []:

        # add the new user to database
        new_user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()

        # Set session for current user
        user_id = new_user.user_id

        session['current_user'] = user_id
        flash("Welcome new super-rater of super-movies. You're SUPER.")

        return redirect('/users/' + str(user_id))

    # Current user is already in DB -- check for password verification    
    else:

        current_user_email = current_user[0].email
        current_user_pw = current_user[0].password
        current_user_id = current_user[0].user_id

        if password == current_user_pw:
            session['current_user'] = current_user_id
            flash("Welcome back!  You're logged in!")

            user_id = current_user[0].user_id

            return redirect('/users/' + str(user_id))

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
