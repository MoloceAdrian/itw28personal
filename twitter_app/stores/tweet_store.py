from typing import List, Dict

from twitter_app.models.tweet import Tweet
from twitter_app.models.user import User
from twitter_app.twitter_api_client import get_tweets


class TweetStore:
    """SQL Wrapper for us to interact with the database."""

    def __init__(self, db):
        """Init.
        Args:
            db: SQLAlchemy - database object
        """
        self.__db = db

    def create_tweet(self, user: User, tweet_json: Dict) -> Tweet:
        """Create a Tweet object given a json with data.

        Args:
            user: User - user object to get the user_id and number of followers
            tweet_json: Dict - dictionary with relevant tweet data.
        Returns:
            Tweet
        """
        return Tweet(
            id=tweet_json["id"],
            text=tweet_json["text"],
            number_of_favorites=tweet_json["favorite_count"],
            number_of_retweets=tweet_json["retweet_count"],
            parent_tweet_id=tweet_json["in_reply_to_status_id"],
            user_id=user.id,
            engagement_score=(
                tweet_json["favorite_count"] + tweet_json["retweet_count"]
            )
            / user.number_of_followers,
        )

    def upsert(self, tweet: Tweet):
        """Insert or update a tweet.

        Searches the database to check if the tweet exists. Updates it if so otherwise it is inserted.

        Args:
            tweet: Tweet
        """
        existing_tweet = Tweet.query.filter_by(id=tweet.id).first()
        if existing_tweet:
            self.__db.session.delete(existing_tweet)
        self.__db.session.add(tweet)
        self.__db.session.commit()

    def save_tweets_for_user(self, user: User, tweets: List[dict]):
        """Save a list of tweets for an user.

        Args:
            user: User
            tweets: List[Dict] list of tweet json data
        """
        for tweet_json in tweets:
            tweet = self.create_tweet(user, tweet_json)
            self.upsert(tweet)

    def delete(self, tweet_id: int):
        """Delete a tweet.

        Args:
            tweet_id: int - the id of the tweet.
        """
        tweet = Tweet.query.get_or_404(tweet_id)
        self.__db.session.delete(tweet)
        self.__db.session.commit()
