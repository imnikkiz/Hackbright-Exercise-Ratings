from flask import Flask, render_template, redirect, request, flash, session
import model
import os
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user = model.session.query(model.User).filter(model.User.email==user_email).one()
    print user
    return render_template("welcome.html")

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
    return render_template("welcome.html")

@app.route("/all_users")
def show_all_users():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("all_users.html", users=user_list)

@app.route("/user_profile")
def show_user_profile():
    return render_template("user_profile.html")

@app.route("/my_profile")
def show_my_profile():
    return render_template("user_profile.html")

@app.route("/all_movies")
def show_all_movies():
    return render_template("all_movies.html")

@app.route("/movie_profile")
def show_movie_profile():
    return render_template("movie_profile.html")







if __name__ == "__main__":
    app.run(debug=True)

