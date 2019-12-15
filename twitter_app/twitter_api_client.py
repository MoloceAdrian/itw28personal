import base64
from typing import Dict, List

import requests

from config import CONSUMER_KEY, CONSUMER_SECRET, TWITTER_AUTH_URL

TWEET_LIMIT = 25
TWITTER_RESULT_TYPE = "latest"

bearer_token = CONSUMER_KEY + ":" + CONSUMER_SECRET
base64_encoded_bearer_token = base64.b64encode(bearer_token.encode("utf-8"))
headers = {
    "Authorization": "Basic " + base64_encoded_bearer_token.decode("utf-8") + "",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Content-Length": "29",
}
statuses_user_timeline_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
collection_entries_url = "https://api.twitter.com/1.1/collections/entries.json"


def get_bearer_access_token() -> str:
    """Make a request to twitters Auth page to get a bearer token.

    Returns:
        bearer_token: str
    """
    bearer_response = requests.post(
        TWITTER_AUTH_URL, headers=headers, data={"grant_type": "client_credentials"}
    )
    return bearer_response.json()["access_token"]


def get_tweets(
    screen_name: str, result_type=TWITTER_RESULT_TYPE, count=TWEET_LIMIT
) -> List[Dict]:
    """Retrieve a list of tweets using the twitter API.

    Args:
        screen_name: str - handle or username in twitter terms
        result_type: str - latest, current, etc
        count: int - number of results to return
    Returns:
        tweets: List[Dict]
    """
    search_params = {
        "screen_name": screen_name,
        "result_type": result_type,
        "count": count,
    }
    response_tweets = requests.get(
        statuses_user_timeline_url,
        headers={"Authorization": "Bearer {}".format(get_bearer_access_token())},
        params=search_params,
    )
    return response_tweets.json()
