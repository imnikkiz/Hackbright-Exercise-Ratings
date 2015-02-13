from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import correlation

engine = create_engine("sqlite:///ratings.db", echo=True)
session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit = False, 
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property()

# To recreate db, run:
# Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True, unique=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def __repr__(self):
        return "<User id=%d email=%s password=%s age=%d zipcode=%s>" % (
            self.id, self.email, self.password, self.age, self.zipcode)

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) \
            for r in other_ratings ]
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        return numerator/denominator

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    title = Column(String(64))
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(64), nullable=True)

    def __repr__(self):
        return "<Movie id=%d title=%s released_at=%s imdb_url=%s>" % (
            self.id, self.title, str(self.released_at), self.imdb_url)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=True)    

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

    def __repr__(self):
        return "<Rating id=%d movie_id=%d user_id=%d rating=%d user=%s movie=%s>" % (
            self.id, self.movie_id, self.user_id, self.rating, self.user, self.movie)

def main():
    pass


if __name__ == "__main__":
    main()

# TODO
# datetime format