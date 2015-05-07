"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import correlation

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

# Delete this line and put your User/Movie/Ratings model classes here.
class User(db.Model):
    """User of ratings website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id = %s email = %s>" % (self.user_id, self.email)

    def similarity(self, other_rating):
        this_user_rating_dict = {}
        paired_list = []

        this_user_rating_obj = self.ratings

        for r in this_user_rating_obj:
            this_user_rating_dict[r.movie_id] = r.score


        for r in other_rating.ratings:
            movie_id = r.movie_id
            if this_user_rating_dict.get(movie_id):
                paired_list.append((r.score, this_user_rating_dict[movie_id]))

        if paired_list:
            return correlation.pearson(paired_list)
        else:
            return 0.0
        



class Movie(db.Model):
    """Movie of ratings website"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_title = db.Column(db.String(64), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Movie movie_id = %s movie_title = %s>" % (self.movie_id, self.movie_title)

class Rating(db.Model):
    """Ratings from rating website"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship("User",
                            backref=db.backref("ratings", order_by=rating_id))

    movie = db.relationship("Movie",
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Rating rating_id = %s score = %s user_id = %s>" % (self.rating_id, self.score, self.user_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."