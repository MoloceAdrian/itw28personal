import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
TWITTER_AUTH_URL = os.getenv("TWITTER_AUTH_URL", "https://api.twitter.com/oauth2/token")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
