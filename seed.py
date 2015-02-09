import model
import csv

def load_users(session):
    user_file = open("./seed_data/u.user")
    for line in user_file:
        line = line.strip()
        line = line.split("|")


        user = model.User()
        user.age = line[1].decode("latin-1")
        user.zipcode = line[4].decode("latin-1")


        session.add(user)
        
    session.commit()

def load_movies(session):
    movie_file = open("./seed_data/u.item")
    for line in movie_file:
        line = line.strip()
        line = line.split("|")
        

        movie = model.Movie()
        movie.title = line[1].decode("latin-1")
        movie.release_date = line[2].decode("latin-1")
        movie.imdb_url = line[4].decode("latin-1")

        session.add(movie)

    session.commit()

def load_ratings(session):
    rating_file = open("./seed_data/u.data")
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
    # load_users(session)
    # load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)
