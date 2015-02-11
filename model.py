from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

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
        return "<User id=%d email=%s password=%s age=%d zipcode=%s" % (
            self.id, self.email, self.password, self.age, self.zipcode)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    title = Column(String(64))
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(64), nullable=True)

    def __repr__(self):
        return "<Movie id=%d title=%s released_at=%s imdb_url=%s" % (
            self.id, self.title, str(self.released_at), self.imdb_url)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=True)    

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))


def main():
    pass


if __name__ == "__main__":
    main()
