from flask import Flask, render_template, redirect, request, flash, session
import model
import os
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/")
def index():
    return render_template("welcome.html")

# Sign Up    

@app.route("/signup", methods=['GET'])
def show_signup():
    return render_template("signup.html")


@app.route("/signup", methods=['POST'])
def signup():
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user_age = request.form.get('age')
    user_zipcode = request.form.get('zipcode')

    new_user = model.User(email=user_email, password=user_password)
    if user_age:
        new_user.age = user_age
    if user_zipcode:
        new_user.zipcode = user_zipcode
    
    model.session.add(new_user)

    try:
        model.session.commit()
    except IntegrityError:
        flash("Email already in database. Please try again.")
        return show_signup()

    flash("Signup successful")
    session['user'] = user_email
    return render_template("welcome.html")

# Log In / Log Out


@app.route("/login", methods=["GET"])
def show_login():
    if session.get('user'):
        flash("You have successfully logged out.")
        session.clear()
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    users = model.session.query(model.User)

    try:
        user = users.filter(model.User.email==user_email,
                            model.User.password==user_password
                            ).one()
    except InvalidRequestError:
        flash("That email or password was incorrect. " 
            "Please check your login credentials or sign up.")
        return render_template("login.html")

    session['user'] = user_email
    session['count'] = 0
    
    return render_template("welcome.html")

# All Users / User Profile

@app.route("/all_users")
def show_all_users():
    users = model.session.query(model.User)
    user_list = users.filter(model.User.email.isnot(None)).all()
    return render_template("all_users.html", users=user_list)

@app.route("/user_profile", methods=["GET"])
def show_user_profile():
    email = request.args.get("email")   
    users = model.session.query(model.User)
    user = users.filter(model.User.email == email).one()
    heading = "%s's Profile" % (email)
    return render_template("user_profile.html", user=user, 
                                                heading=heading)

@app.route("/my_profile")
def show_my_profile():
    if session.get('user'):
        email = session.get('user')
        users = model.session.query(model.User)
        user = users.filter(model.User.email == email).one()
        heading = "My Profile"
        return render_template("user_profile.html", user=user,
                                                    heading=heading)
    flash("Please log in.")
    return show_login()

# All Movies / Movie Profile

@app.route("/all_movies")
def show_all_movies():
    if session.get('user'):
        count = session.get('count')
    else:
        count = 0
    movies = model.session.query(model.Movie)
    movies_list = movies.offset(count).limit(10).all()
    print movies_list

    if session.get('user'):
        session['count'] += 10


    return render_template("all_movies.html", movies=movies_list)

@app.route("/movie_profile", methods=["GET"])
def show_movie_profile():
    title = request.args.get("title")
    movies = model.session.query(model.Movie)
    movie = movies.filter(model.Movie.title == title).one()
    return render_template("movie_profile.html", movie=movie)


if __name__ == "__main__":
    app.run(debug=True)

