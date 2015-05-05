"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
import datetime

def load_users():
    """Load users from u.user into database."""

    users_file = open("./seed_data/u.user")

    for line in users_file:
        line = line.strip().split("|")
        a_user = User(age = line[1], zipcode = line[4])
        db.session.add(a_user)

    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    movies_file = open('./seed_data/u.item')

    for line in movies_file:
        line = line.strip().split("|")

        if line[2] == "":
            date = None
        else:
            date = datetime.datetime.strptime(line[2], '%d-%b-%Y')

        a_movie = Movie(
            movie_title=line[1][:-7].decode("latin-1"),
            released_at=date, imdb_url=line[4])
        db.session.add(a_movie)

    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    ratings_file = open("./seed_data/u.data")

    for line in ratings_file:
        line = line.strip().split()
        a_rating = Rating(user_id = line[0], movie_id = line[1], score = line[2])
        db.session.add(a_rating)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
