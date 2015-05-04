"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime, strptime

def load_users():
    """Load users from u.user into database."""

    users_file = open("./seed_data/u.user")

    for line in users_file:
        line = line.strip().split("|")
        a_user = User(user_id = line[0], age = line[1], zipcode = line[4])
        db.session.add(a_user)

    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    movies_file = open('/seed_data/u.item')

    for line in movies_file:
        line = line.strip.split("|")
        date = " ".join(line[2].split("-"))
        date = datetime.strptime(date, '%b, %d, %Y')
        # a_movie = Movie(movie_id=line[0], movie_title=line[1][:-7], released_at=line[])


def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    # load_movies()
    # load_ratings()
