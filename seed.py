import model
import csv
from datetime import datetime
import time

def load_users(session):
    with open("./seed_data/u.user") as user_file:
        for line in user_file:
            line = line.strip()
            line = line.split("|")

            user = model.User()
            user.age = line[1].decode("latin-1")
            user.zipcode = line[4].decode("latin-1")
            
            session.add(user)
    session.commit()

def load_movies(session):
    with open("./seed_data/u.item") as movie_file:
        for line in movie_file:
            line = line.strip()
            line = line.split("|")
            
            movie = model.Movie()

            title_date = line[1].decode("latin-1")
            title_date = title_date.split("(")
            movie.title = title_date[0].strip()


            release_date = line[2].decode("latin-1")
            if release_date != "":
                movie.released_at = datetime.strptime(release_date, "%d-%b-%Y")

            movie.imdb_url = line[4].decode("latin-1")

            session.add(movie)
    session.commit()


def load_ratings(session):
    with open("./seed_data/u.data") as rating_file:
        for line in rating_file:
            line = line.strip()
            line = line.split()

            rating = model.Rating()
            rating.user_id = line[0].decode("latin-1")
            rating.movie_id = line[1].decode("latin-1")
            rating.rating = line[2].decode("latin-1")

            session.add(rating)

    session.commit()


def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    main(model.session)
