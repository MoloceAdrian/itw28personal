from twitter_app import db


class Tweet(db.Model):
    """Tweet to SQLAlchemy mapper."""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    number_of_favorites = db.Column(db.Integer, nullable=False)
    number_of_retweets = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    parent_tweet_id = db.Column(db.Integer, nullable=True)
    engagement_score = db.Column(db.Float, nullable=False)
