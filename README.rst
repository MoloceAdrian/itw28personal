itw28
=====

This project uses the twitter api to get data about twitter users and their tweets so that the users of this application
can download and review these tweets whenever they want.

If you're a developer then check out the project setup below:

Using the project
=================

Create a virtual environment for example run:

``virtualenv --python=python3.7 venv``

Make sure to use your new environment:

``source venv/bin/activate``

Install the required libraries:

``pip install -r requirements.txt``

Run the project with:

``python run.py``

NOTE
====

Don't forget to create an .env file and configure the required variables such as
CONSUMER_KEY and CONSUMER_SECRET.

Functioning features
====================

* Retrieve the latest 25 tweets given a twitter screen name
* Save all the returned tweets that belong to that handle, so they can be reviewed later
* Assign an engagement_score for each tweet, computed as follows for each tweet
* View a list of the users/handles for which we have already downloaded the tweets and the count of imported messages for each one of them
* View a list of the tweets that were already downloaded. List is ordered descending based on number of favorites (most favorite, at the top). If 2 tweets have the same favorite count, next determinator is number of retweets. For each tweet the engagement_score is also displayed.
* Delete tweets that were already downloaded.
* Ability to import and save a list of handles/screen_names from a CSV file
* Application runs a periodic task that can download new tweets for all saved handles

Non-functioning features
========================

* Build relationship tree for tweets. Ex: if a tweet is a reply to a different one, store the parent as well + the owner of the parent twee
* Functionality to search through the content the saved tweets