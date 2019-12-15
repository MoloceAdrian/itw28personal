from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "b07f8863-a6be-4d61-81f6-7120ad5ba7e2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///twitter.db"
db = SQLAlchemy(app)

from twitter_app import routes
