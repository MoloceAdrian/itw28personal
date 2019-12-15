from logging import getLogger
from typing import List, Dict

from flask import render_template, url_for, redirect, request, flash

from config import LOG_LEVEL
from twitter_app import app, db
from twitter_app.forms import ScreenNameForm, UploadCSVFileForm
from twitter_app.models.user import User
from twitter_app.models.tweet import Tweet
from twitter_app.stores.tweet_store import TweetStore
from twitter_app.stores.user_store import UserStore
from twitter_app.twitter_api_client import get_tweets


logging = getLogger(__name__)
USER_STORE = UserStore(db)
TWEET_STORE = TweetStore(db)


def update_all_user_tweets():
    """Gets a list of all users and pulls the latest tweets for each."""
    users = User.query.all()
    for user in users:
        tweets = get_tweets(screen_name=user.screen_name)
        TWEET_STORE.save_tweets_for_user(user, tweets)


@app.route("/")
@app.route("/home")
def home():
    """Display the empty Home page"""
    return render_template("layout.html")


def save_user_and_tweets(tweets: List[Dict]):
    """Save a new user and it's tweets.

    Args:
        tweets: List[Dict] - list of json objects with tweet data
    """
    try:
        user_json = tweets[0]["user"]
        user = USER_STORE.create_user(user_json)
        USER_STORE.upsert(user)
        TWEET_STORE.save_tweets_for_user(user, tweets)
        return redirect(url_for("view_user_tweets", user_id=user.id))
    except (KeyError, IndexError):
        flash("The account could not be retrieved.", "failure")


@app.route("/save_tweets_for_user", methods=["GET", "POST"])
def save_tweets_for_user():
    """Get the twitter screen name for a user and download latest tweets."""
    form = ScreenNameForm()
    if form.validate_on_submit():
        tweets = get_tweets(form.screen_name.data)
        save_user_and_tweets(tweets)
    return render_template("get_tweets.html", title="Get Tweets", form=form)


@app.route("/users", methods=["GET"])
def view_users():
    """Display a list of all the users."""
    users = User.query.all()
    return render_template("users.html", title="View Users", users=users)


def upload_users_from_csv(csv: str):
    """Read a list of users from a csv and save them in the database.

    Args:
        csv: str - string data from the csv file uploaded by user.
    """
    for screen_name in csv.split("\n"):
        tweets = get_tweets(screen_name=screen_name)
        save_user_and_tweets(tweets)


@app.route("/users/upload", methods=["GET", "POST"])
def upload_csv():
    """Get a csv file with the twitter screen name of users and save them to our database."""
    form = UploadCSVFileForm()
    if form.validate_on_submit():
        if form.csv.data:
            logging.debug(f"Got this file: {form.csv.data.filename}")
            upload_users_from_csv(form.csv.data.read().decode("utf-8"))
            return redirect(url_for("view_users"))
        logging.debug("No file received.")
    return render_template("upload_csv.html", title="Upload Users", form=form)


@app.route("/tweet", methods=["GET"])
def view_tweets():
    """Display the a page with all the sorted tweets in the database.

        The sorting algorithm is the number of favorites then the number of retweets.
    """
    page = request.args.get("page", 1, int)
    tweets = Tweet.query.order_by(
        Tweet.number_of_favorites.desc(), Tweet.number_of_retweets.desc()
    ).paginate(page=page, per_page=10)
    return render_template("tweet.html", title="View All Tweets", tweets=tweets)


@app.route("/tweet/<int:user_id>/view", methods=["GET"])
def view_user_tweets(user_id):
    """View all the tweets for a specific user.

    Args:
        user_id: int - the id of the user for which to display the tweets.
    """
    tweets = Tweet.query.filter_by(user_id=user_id)
    user = User.query.filter_by(id=user_id).first()
    return render_template(
        "user_tweets.html", title="View User Tweets", tweets=tweets, author=user.name, tweet_count=tweets.count()
    )


@app.route("/tweet/<int:tweet_id>/delete", methods=["GET"])
def delete_tweet(tweet_id):
    """Get the id of a tweet and delete it.

    Args:
        tweet_id: int - the id of the tweet to delete.
    """
    TWEET_STORE.delete(tweet_id)
    return redirect(url_for("view_tweets"))
