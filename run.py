import time

from twitter_app import app
from twitter_app.routes import update_all_user_tweets


PERIODIC_TASK_INTERVAL = 1800


if __name__ == "__main__":
    app.run(debug=True)
    while True:
        update_all_user_tweets()
        time.sleep(PERIODIC_TASK_INTERVAL)
