from twitter_app import db


class User(db.Model):
    """User to SQLAlchemy mapper."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    screen_name = db.Column(db.String(20), unique=True, nullable=False)
    number_of_followers = db.Column(db.Integer, nullable=False)
    tweets = db.relationship("Tweet", backref="owner", lazy=True)
